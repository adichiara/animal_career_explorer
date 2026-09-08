#!/usr/bin/env python3
"""Scrape the public AZA Jobs board into the project's market_job_postings table.

Design goals
------------
* Enumerate every listing shown by the AZA Jobs board, including pagination.
* Follow each standardized detail page.
* Store normalized facts and concise derived summaries, not full copyrighted page text.
* Preserve provenance, dates, a content hash, and scrape status.
* Resume safely after interruption and upsert changed postings.
* Respect AZA's published generic crawl-delay by default (30 seconds).

Run in a network-enabled environment with Playwright installed:
    pip install playwright
    playwright install chromium
    python scripts/scrape_aza_jobs.py --db database/careers.sqlite

For a quick parser/browser test only:
    python scripts/scrape_aza_jobs.py --db database/careers.sqlite --limit 3
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sqlite3
import sys
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import parse_qs, urlparse

try:
    from playwright.async_api import async_playwright, Page
except Exception:  # pragma: no cover
    async_playwright = None
    Page = object

BASE_URL = "https://www.aza.org/Jobs"
SOURCE_ID = "source_aza_jobs_board"
DEFAULT_DELAY = 30.0

DUTY_RULES = {
    "husbandry": ["husbandry", "animal care", "care for animals", "daily care"],
    "feeding_nutrition": ["feed", "diet", "nutrition", "food preparation", "prepare food"],
    "cleaning_sanitation": ["clean", "sanitation", "disinfect", "enclosure maintenance"],
    "behavior_observation": ["observe", "behavior", "behaviour", "behavioral"],
    "welfare_wellbeing": ["welfare", "wellbeing", "well-being"],
    "training": ["train", "training", "positive reinforcement", "operant conditioning"],
    "enrichment": ["enrichment"],
    "recordkeeping": ["record", "zims", "documentation", "data entry"],
    "guest_education": ["guest", "visitor", "public", "interpret", "education", "presentation"],
    "research": ["research", "study", "data collection", "protocol"],
    "conservation": ["conservation", "species survival", "ssp", "safe program"],
    "veterinary_support": ["veterinary", "medical", "diagnostic", "treatment", "hospital"],
    "water_quality_life_support": ["water quality", "life support", "aquatic systems", "lss"],
    "diving": ["scuba", "dive", "diving"],
    "fieldwork": ["field work", "fieldwork", "field survey", "monitoring", "telemetry"],
    "supervision": ["supervise", "lead staff", "manage staff", "direct reports"],
    "horticulture": ["horticulture", "plants", "gardening", "landscape"],
    "administration": ["budget", "grant", "administration", "financial", "project management"],
}

SKILL_RULES = {
    "animal_handling": ["animal handling", "work with live animals", "handle animals"],
    "animal_behavior": ["animal behavior", "behaviour", "behavioral principles"],
    "husbandry": ["husbandry"],
    "public_speaking": ["public speaking", "presentation", "interpretation", "guest interaction"],
    "written_communication": ["written communication", "writing skills", "report writing"],
    "interpersonal": ["interpersonal", "teamwork", "collaborative", "communication skills"],
    "computer_office": ["microsoft", "office 365", "excel", "word", "outlook"],
    "zims": ["zims"],
    "data_analysis": ["data analysis", "statistics", "statistical", "r software", "python"],
    "gis": ["gis", "arcgis", "spatial"],
    "telemetry": ["telemetry", "radio tracking", "gps tracking"],
    "water_quality": ["water quality"],
    "life_support_systems": ["life support systems", "lss"],
    "leadership": ["leadership", "supervisory", "supervision", "manage staff"],
    "project_management": ["project management", "project manager"],
}

CREDENTIAL_RULES = {
    "drivers_license": ["driver's license", "drivers license", "driver’s license"],
    "scuba": ["scuba"],
    "cpr_first_aid": ["cpr", "first aid"],
    "veterinary_technician_license": ["licensed veterinary technician", "credentialed veterinary technician", "lvt", "cvt", "rvt"],
    "rabies_vaccination": ["rabies vaccination", "rabies vaccine"],
}

POSITION_RULES = [
    ("internship", ["internship", "intern "]),
    ("seasonal", ["seasonal"]),
    ("temporary", ["temporary", "temp "]),
    ("part-time", ["part-time", "part time", "parttime", " pt "]),
    ("full-time", ["full-time", "full time", "fulltime", " ft "]),
]

DEGREE_PATTERNS = [
    ("doctorate", re.compile(r"\b(ph\.?d\.?|doctorate|doctoral degree)\b", re.I)),
    ("masters", re.compile(r"\b(master'?s|masters|m\.?s\.?|m\.?a\.?)\b", re.I)),
    ("bachelors", re.compile(r"\b(bachelor'?s|bachelors|b\.?s\.?|b\.?a\.?)\b", re.I)),
    ("associates", re.compile(r"\b(associate'?s|associates|a\.?s\.?)\b", re.I)),
    ("high_school", re.compile(r"\b(high school diploma|ged|high school equivalent)\b", re.I)),
]

@dataclass
class Listing:
    job_id: str
    title: str
    employer: str
    location: str
    posted_date: Optional[str]
    aza_member: Optional[int]
    url: str
    listing_page: int


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def parse_us_date(text: str | None) -> Optional[str]:
    if not text:
        return None
    text = normalize_space(text).replace("Sept ", "Sep ")
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def job_id_from_url(url: str) -> Optional[str]:
    q = parse_qs(urlparse(url).query)
    vals = q.get("job") or q.get("Job")
    return vals[0] if vals else None


def split_location(location: str):
    x = normalize_space(location)
    m = re.match(r"^(.*?),\s*([A-Z]{2}|[A-Za-z .'-]+)$", x)
    if m:
        return m.group(1).strip(), m.group(2).strip(), "US"
    return x or None, None, "US"


def extract_tags(text: str, rules: dict[str, list[str]]) -> list[str]:
    s = f" {normalize_space(text).lower()} "
    return sorted(k for k, words in rules.items() if any(w.lower() in s for w in words))


def detect_position_type(title: str, text: str) -> Optional[str]:
    s = f" {title} {text} ".lower()
    for label, words in POSITION_RULES:
        if any(w in s for w in words):
            return label
    return None


def detect_employment_status(text: str) -> Optional[str]:
    s = text.lower()
    if "non-exempt" in s or "nonexempt" in s:
        return "non-exempt"
    if re.search(r"\bexempt\b", s):
        return "exempt"
    return None


def detect_degree(text: str) -> Optional[str]:
    # Minimum, not highest: inspect in ascending order after finding all mentions.
    found = []
    order = {"high_school": 0, "associates": 1, "bachelors": 2, "masters": 3, "doctorate": 4}
    for level, pat in DEGREE_PATTERNS:
        if pat.search(text):
            found.append(level)
    return min(found, key=lambda x: order[x]) if found else None


def detect_degrees_all(text: str) -> list[str]:
    order = {"high_school": 0, "associates": 1, "bachelors": 2, "masters": 3, "doctorate": 4}
    found = [level for level, pat in DEGREE_PATTERNS if pat.search(text)]
    return sorted(set(found), key=lambda x: order[x])


def detect_education_field(text: str) -> Optional[str]:
    patterns = [
        r"(?:degree|major)\s+in\s+([A-Za-z ,/&-]{3,90})",
        r"(?:bachelor'?s|master'?s|associate'?s)\s+(?:degree\s+)?in\s+([A-Za-z ,/&-]{3,90})",
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            value = re.split(r"[.;\n]", m.group(1))[0]
            value = re.sub(r"\b(required|preferred|desired|or related field|or closely related field)\b.*$", "", value, flags=re.I)
            return normalize_space(value).strip(" ,/-")[:120] or None
    return None


def detect_experience_years(text: str) -> Optional[float]:
    vals = []
    for m in re.finditer(r"(?<!\d)(\d+(?:\.\d+)?)\s*(?:\+\s*)?(?:years?|yrs?)\s+(?:of\s+)?(?:relevant\s+|professional\s+|paid\s+|hands[- ]on\s+|zoo\s+|animal\s+)?experience", text, re.I):
        vals.append(float(m.group(1)))
    # Also handle 'minimum of X years'.
    for m in re.finditer(r"(?:minimum(?:\s+of)?|at least)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)", text, re.I):
        vals.append(float(m.group(1)))
    return min(vals) if vals else None


def detect_salary(text: str):
    """Return min,max,unit,raw using conservative patterns."""
    candidates = []
    # $16.20-$18.50/hour; $45,000 - $55,000 per year
    pat = re.compile(
        r"\$\s*([\d,]+(?:\.\d+)?)\s*(?:-|–|to)\s*\$?\s*([\d,]+(?:\.\d+)?)\s*(?:/|per\s+)?(hour|hr|year|yr|annual|annually)?",
        re.I,
    )
    for m in pat.finditer(text):
        a, b = float(m.group(1).replace(",", "")), float(m.group(2).replace(",", ""))
        unit = (m.group(3) or "").lower()
        if unit in ("hour", "hr"): unit = "hour"
        elif unit in ("year", "yr", "annual", "annually"): unit = "year"
        else:
            unit = "year" if max(a, b) > 500 else "hour"
        candidates.append((a, b, unit, normalize_space(m.group(0))))
    # single stated rate
    pat2 = re.compile(r"\$\s*([\d,]+(?:\.\d+)?)\s*(?:/|per\s+)(hour|hr|year|yr)", re.I)
    for m in pat2.finditer(text):
        a = float(m.group(1).replace(",", "")); unit = "hour" if m.group(2).lower() in ("hour", "hr") else "year"
        candidates.append((a, a, unit, normalize_space(m.group(0))))
    if not candidates:
        return None, None, None, None
    # Prefer text close to explicit salary/compensation/pay labels.
    for c in candidates:
        idx = text.lower().find(c[3].lower())
        window = text[max(0, idx-80):idx].lower()
        if any(k in window for k in ("salary", "compensation", "pay", "rate")):
            return c
    return candidates[0]


def extract_named_date(text: str, labels: Iterable[str]) -> Optional[str]:
    for label in labels:
        m = re.search(rf"{re.escape(label)}\s*:?[\s\xa0]*([A-Za-z]+\s+\d{{1,2}}(?:st|nd|rd|th)?[,]?\s+\d{{4}}|\d{{1,2}}/\d{{1,2}}/\d{{2,4}})", text, re.I)
        if m:
            v = re.sub(r"(\d)(st|nd|rd|th)", r"\1", m.group(1), flags=re.I)
            return parse_us_date(v)
    return None


def section_between(text: str, start_labels: list[str], end_labels: list[str]) -> str:
    lower = text.lower()
    starts = [(lower.find(x.lower()), x) for x in start_labels if lower.find(x.lower()) >= 0]
    if not starts:
        return ""
    start_idx, label = min(starts, key=lambda x: x[0])
    start_idx += len(label)
    ends = [lower.find(x.lower(), start_idx) for x in end_labels]
    ends = [x for x in ends if x >= 0]
    end_idx = min(ends) if ends else len(text)
    return text[start_idx:end_idx].strip()


def build_duties_summary(tags: list[str]) -> Optional[str]:
    names = {
        "husbandry": "daily animal husbandry",
        "feeding_nutrition": "feeding and diet preparation",
        "cleaning_sanitation": "cleaning and sanitation",
        "behavior_observation": "behavioral observation",
        "welfare_wellbeing": "animal welfare monitoring",
        "training": "animal training",
        "enrichment": "enrichment",
        "recordkeeping": "recordkeeping",
        "guest_education": "guest education",
        "research": "research/data collection",
        "conservation": "conservation work",
        "veterinary_support": "veterinary/medical support",
        "water_quality_life_support": "water-quality/life-support work",
        "diving": "diving",
        "fieldwork": "fieldwork/monitoring",
        "supervision": "staff supervision",
        "horticulture": "horticulture",
        "administration": "administration/project management",
    }
    vals = [names[t] for t in tags if t in names]
    return "Primary duties include " + ", ".join(vals[:7]) + "." if vals else None


def build_requirements_summary(degree, field, years, skills, credentials) -> Optional[str]:
    parts = []
    if degree:
        label = degree.replace("_", " ")
        parts.append(f"minimum education identified: {label}" + (f" ({field})" if field else ""))
    if years is not None:
        parts.append(f"minimum experience identified: {years:g} year(s)")
    if skills:
        parts.append("skills emphasized: " + ", ".join(skills[:6]))
    if credentials:
        parts.append("credentials/requirements noted: " + ", ".join(credentials[:5]))
    return "; ".join(parts).capitalize() + "." if parts else None


def ensure_schema(con: sqlite3.Connection, project_root: Path):
    migration = project_root / "database" / "migration_aza_market_jobs.sql"
    con.executescript(migration.read_text(encoding="utf-8"))
    # Forward-compatible column additions for databases created before this migration revision.
    existing = {r[1] for r in con.execute("PRAGMA table_info(market_job_postings)")}
    for name, coltype in {
        "education_requirements_json": "TEXT",
        "experience_requirements_json": "TEXT",
    }.items():
        if name not in existing:
            con.execute(f"ALTER TABLE market_job_postings ADD COLUMN {name} {coltype}")
    con.execute(
        """INSERT OR IGNORE INTO sources
        (source_id, organization, source_type, title, url, retrieved_date, authority_tier, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (SOURCE_ID, "Association of Zoos & Aquariums", "job_board", "AZA Jobs board", BASE_URL, utcnow()[:10], "B", "Public AZA employment listings; complete board snapshots are stored in market_job_postings."),
    )
    con.commit()


async def visible_job_links(page: Page):
    anchors = page.locator('a[href*="job="]')
    out = []
    seen = set()
    for i in range(await anchors.count()):
        a = anchors.nth(i)
        href = await a.get_attribute("href")
        title = normalize_space(await a.inner_text())
        if not href or not title:
            continue
        url = href if href.startswith("http") else "https://www.aza.org" + (href if href.startswith("/") else "/" + href)
        jid = job_id_from_url(url)
        if jid and jid not in seen:
            seen.add(jid); out.append((jid, title, url, a))
    return out


async def listing_from_anchor(anchor_tuple, page_no: int) -> Listing:
    jid, title, url, anchor = anchor_tuple
    # Walk upward looking for a row-like ancestor whose text contains a posted date.
    employer = ""
    location = ""
    date_text = None
    member = None
    row_text = ""
    for xpath in ["xpath=ancestor::tr[1]", "xpath=ancestor::*[self::div or self::li][1]"]:
        try:
            row = anchor.locator(xpath)
            if await row.count():
                row_text = normalize_space(await row.first.inner_text())
                if re.search(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4}", row_text):
                    break
        except Exception:
            pass
    # If this really is a table, cell positions are more reliable.
    try:
        tr = anchor.locator("xpath=ancestor::tr[1]")
        if await tr.count():
            cells = tr.locator("td")
            vals = [normalize_space(await cells.nth(i).inner_text()) for i in range(await cells.count())]
            if len(vals) >= 4:
                first = vals[0]
                # first cell often concatenates title + organization. Remove title prefix.
                employer = normalize_space(first[len(title):]) if first.startswith(title) else ""
                location, date_text = vals[1], vals[2]
                member = 1 if vals[3].lower() == "yes" else 0 if vals[3].lower() == "no" else None
    except Exception:
        pass
    # Fallback parses common rendered row text.
    if not date_text:
        m = re.search(r"(.*?),\s*([A-Z]{2})\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4})\s+(Yes|No)\s*$", row_text)
        if m:
            location = f"{m.group(1).strip()}, {m.group(2)}"
            date_text = m.group(3)
            member = 1 if m.group(4) == "Yes" else 0
    return Listing(jid, title, employer or "Unknown employer", location, parse_us_date(date_text), member, url, page_no)


async def enumerate_all_listings(page: Page) -> list[Listing]:
    """Enumerate all visible board pages by clicking numeric/next pagination controls.

    The AZA board currently renders pagination client-side, so this deliberately
    follows the UI rather than guessing undocumented query parameters.
    """
    await page.goto(BASE_URL, wait_until="networkidle", timeout=90000)
    all_listings: dict[str, Listing] = {}
    visited_signatures = set()
    page_no = 1
    while True:
        await page.wait_for_timeout(800)
        links = await visible_job_links(page)
        signature = tuple(x[0] for x in links[:5])
        if not links or signature in visited_signatures:
            break
        visited_signatures.add(signature)
        for a in links:
            listing = await listing_from_anchor(a, page_no)
            all_listings[listing.job_id] = listing

        before = set(x[0] for x in links)
        clicked = False
        # Prefer exact next page number; fall back to a Next link.
        candidates = [
            page.get_by_role("link", name=str(page_no + 1), exact=True),
            page.get_by_role("button", name=str(page_no + 1), exact=True),
            page.get_by_role("link", name=re.compile(r"^next$", re.I)),
            page.get_by_role("button", name=re.compile(r"^next$", re.I)),
        ]
        for loc in candidates:
            try:
                count = await loc.count()
                for i in range(count):
                    el = loc.nth(i)
                    if not await el.is_visible():
                        continue
                    await el.click()
                    await page.wait_for_timeout(1500)
                    after = set(x[0] for x in await visible_job_links(page))
                    if after and after != before:
                        clicked = True
                        break
                if clicked:
                    break
            except Exception:
                continue
        if not clicked:
            break
        page_no += 1
    return list(all_listings.values())


async def scrape_detail(page: Page, listing: Listing):
    await page.goto(listing.url, wait_until="networkidle", timeout=90000)
    await page.wait_for_timeout(500)
    body = normalize_space(await page.locator("body").inner_text())
    # Keep no raw body in DB; hash lets us detect changed source content later.
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    # Detail pages use consistent section headings, but individual employers format
    # their prose differently. Isolate the requirement/salary sections first.
    req = section_between(body, ["Experience Required", "Qualifications", "Minimum Qualifications", "Requirements"], ["Salary", "How to Apply", "Job Perks"])
    salary_section = section_between(body, ["Salary"], ["How to Apply", "Job Perks", "Contact"])
    # Duties are detected from the job content before requirements; using full body
    # for tags is intentionally conservative because the summary is derived, not copied.
    duties_region = section_between(body, [listing.title], ["Experience Required", "Qualifications", "Minimum Qualifications", "Requirements", "Salary", "How to Apply"])
    if not duties_region:
        duties_region = body

    duty_tags = extract_tags(duties_region, DUTY_RULES)
    skill_tags = extract_tags(req or body, SKILL_RULES)
    credential_tags = extract_tags(req or body, CREDENTIAL_RULES)
    degree = detect_degree(req or body)
    degrees_all = detect_degrees_all(req or body)
    edu_field = detect_education_field(req or body)
    exp_years = detect_experience_years(req or body)
    pos_type = detect_position_type(listing.title, body)
    employment_status = detect_employment_status(body)
    sal_min, sal_max, sal_unit, sal_raw = detect_salary(salary_section or body)
    closing = extract_named_date(body, ["Closing Date", "Application Deadline", "Deadline"])
    start = extract_named_date(body, ["Anticipated Start Date", "Start Date"])
    schedule_tags = []
    low = body.lower()
    for tag, words in {
        "weekends": ["weekends", "weekend rotation"],
        "holidays": ["holidays"],
        "evenings": ["evenings", "evening shifts"],
        "rotating_shifts": ["rotating shifts", "rotation schedule"],
        "overnight": ["overnight"],
        "travel": ["travel required", "requires travel"],
    }.items():
        if any(w in low for w in words): schedule_tags.append(tag)

    city, state, country = split_location(listing.location)
    return {
        "posting_id": f"aza_{listing.job_id}",
        "source_id": SOURCE_ID,
        "source_external_id": listing.job_id,
        "source_url": listing.url,
        "source_board": "AZA Jobs",
        "title": listing.title,
        "employer": listing.employer,
        "location_text": listing.location,
        "city": city,
        "state_region": state,
        "country": country,
        "posted_date": listing.posted_date,
        "closing_date": closing,
        "anticipated_start_date": start,
        "retrieved_at": utcnow(),
        "last_seen_at": utcnow(),
        "aza_member": listing.aza_member,
        "position_type": pos_type,
        "employment_status": employment_status,
        "salary_min": sal_min,
        "salary_max": sal_max,
        "salary_unit": sal_unit,
        "currency": "USD",
        "salary_raw": sal_raw,
        "education_level_min": degree,
        "education_field": edu_field,
        "education_requirements_json": json.dumps({"levels_mentioned": degrees_all, "field": edu_field}),
        "experience_years_min": exp_years,
        "experience_requirements_json": json.dumps({"minimum_years_identified": exp_years}),
        "experience_summary": f"At least {exp_years:g} year(s) of relevant experience identified." if exp_years is not None else None,
        "duties_summary": build_duties_summary(duty_tags),
        "requirements_summary": build_requirements_summary(degree, edu_field, exp_years, skill_tags, credential_tags),
        "duty_tags_json": json.dumps(duty_tags),
        "skill_tags_json": json.dumps(skill_tags),
        "credential_tags_json": json.dumps(credential_tags),
        "schedule_tags_json": json.dumps(schedule_tags),
        "detail_status": "scraped",
        "active_status": "active",
        "listing_page": listing.listing_page,
        "raw_text_sha256": body_hash,
        "notes": None,
    }


def upsert_posting(con: sqlite3.Connection, row: dict):
    cols = list(row)
    sql = f"INSERT INTO market_job_postings ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)}) " \
          f"ON CONFLICT(posting_id) DO UPDATE SET " + ",".join(f"{c}=excluded.{c}" for c in cols if c != "posting_id")
    con.execute(sql, [row[c] for c in cols])


def insert_listing_stub(con: sqlite3.Connection, listing: Listing):
    now = utcnow(); city, state, country = split_location(listing.location)
    con.execute(
        """INSERT INTO market_job_postings
        (posting_id, source_id, source_external_id, source_url, source_board, title, employer,
         location_text, city, state_region, country, posted_date, retrieved_at, last_seen_at,
         aza_member, detail_status, active_status, listing_page)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(posting_id) DO UPDATE SET
          title=excluded.title, employer=excluded.employer, location_text=excluded.location_text,
          city=excluded.city, state_region=excluded.state_region, posted_date=excluded.posted_date,
          last_seen_at=excluded.last_seen_at, aza_member=excluded.aza_member,
          listing_page=excluded.listing_page, active_status='active'""",
        (f"aza_{listing.job_id}", SOURCE_ID, listing.job_id, listing.url, "AZA Jobs", listing.title,
         listing.employer, listing.location, city, state, country, listing.posted_date, now, now,
         listing.aza_member, "pending", "active", listing.listing_page),
    )


async def main_async(args):
    if async_playwright is None:
        raise SystemExit("Playwright is required. Install with: pip install playwright && playwright install chromium")
    project_root = Path(args.project_root).resolve()
    db_path = Path(args.db).resolve()
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys=ON")
    ensure_schema(con, project_root)

    run_id = "aza_run_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    con.execute("INSERT INTO market_job_scrape_runs (run_id, source_id, started_at, status, crawl_delay_seconds) VALUES (?,?,?,?,?)",
                (run_id, SOURCE_ID, utcnow(), "running", args.delay))
    con.commit()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=not args.headful)
        context = await browser.new_context(
            user_agent="AnimalCareerExplorerResearch/1.0 (+private educational labor-market research; contact via local project)",
            viewport={"width": 1440, "height": 1000},
        )
        list_page = await context.new_page()
        detail_page = await context.new_page()
        listings = await enumerate_all_listings(list_page)
        listings.sort(key=lambda x: (x.posted_date or "", x.job_id), reverse=True)
        if args.limit:
            listings = listings[:args.limit]

        for l in listings:
            insert_listing_stub(con, l)
        con.execute("UPDATE market_job_scrape_runs SET listings_discovered=?, pages_discovered=? WHERE run_id=?",
                    (len(listings), max((x.listing_page for x in listings), default=0), run_id))
        con.commit()

        ok = fail = 0
        for i, listing in enumerate(listings, 1):
            if not args.refresh:
                prior = con.execute("SELECT detail_status, raw_text_sha256 FROM market_job_postings WHERE posting_id=?", (f"aza_{listing.job_id}",)).fetchone()
                if prior and prior[0] == "scraped" and prior[1]:
                    continue
            try:
                row = await scrape_detail(detail_page, listing)
                upsert_posting(con, row); ok += 1
            except Exception as e:
                con.execute("UPDATE market_job_postings SET detail_status='error', notes=? WHERE posting_id=?", (str(e)[:1000], f"aza_{listing.job_id}"))
                fail += 1
            con.execute("UPDATE market_job_scrape_runs SET details_scraped=?, details_failed=? WHERE run_id=?", (ok, fail, run_id))
            con.commit()
            print(f"[{i}/{len(listings)}] {listing.job_id} {listing.title} -> {'ok' if ok+fail==i else 'processed'}", flush=True)
            if i < len(listings) and args.delay > 0:
                await asyncio.sleep(args.delay)

        # Only mark disappeared AZA postings inactive after a complete, un-limited run.
        if not args.limit and fail == 0:
            current_ids = {f"aza_{x.job_id}" for x in listings}
            rows = con.execute("SELECT posting_id FROM market_job_postings WHERE source_id=? AND active_status='active'", (SOURCE_ID,)).fetchall()
            for (pid,) in rows:
                if pid not in current_ids:
                    con.execute("UPDATE market_job_postings SET active_status='not_seen_current_snapshot' WHERE posting_id=?", (pid,))

        con.execute("UPDATE market_job_scrape_runs SET completed_at=?, status=?, details_scraped=?, details_failed=? WHERE run_id=?",
                    (utcnow(), "completed" if fail == 0 else "completed_with_errors", ok, fail, run_id))
        con.commit()
        await browser.close()
    con.close()
    print(f"Run {run_id}: {len(listings)} listings, {ok} detail pages scraped, {fail} errors")


def parse_args():
    here = Path(__file__).resolve()
    root = here.parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=str(root))
    ap.add_argument("--db", default=str(root / "database" / "careers.sqlite"))
    ap.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="seconds between detail requests; default honors AZA robots.txt crawl-delay")
    ap.add_argument("--limit", type=int, default=0, help="testing only: scrape first N listings")
    ap.add_argument("--refresh", action="store_true", help="rescrape details already present")
    ap.add_argument("--headful", action="store_true")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main_async(args))
