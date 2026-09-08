#!/usr/bin/env python3
"""Create conservative, reviewable AZA-to-career match suggestions.

The rules intentionally favor precision over recall.  Every AZA posting receives
a board-scope classification, while only plausible in-scope postings receive
canonical-role suggestions.  Human-reviewed decisions are never overwritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "careers.sqlite"


ROLE_RULES = {
    "Animal behavior research assistant / technician": {
        "title": ["animal behavioral research assistant", "animal behavior research assistant", "behavioral research assistant", "animal behavior technician", "behavior research technician"],
        "tags": ["research", "behavior_observation", "animal_behavior", "data_analysis"],
    },
    "Zookeeper / animal-care specialist": {
        "title": ["zookeeper", "zoo keeper", "animal keeper", "animal care specialist", "wildlife care specialist", "keeper i", "keeper ii", "keeper iii"],
        "tags": ["husbandry", "feeding_nutrition", "cleaning_sanitation", "animal_handling", "recordkeeping"],
    },
    "Aquarist / aquarium animal-care specialist": {
        "title": ["aquarist", "aquarium keeper", "aquarium animal care", "aquatic animal care", "aquarium biologist", "dive coordinator"],
        "tags": ["water_quality_life_support", "diving", "life_support_systems", "water_quality"],
    },
    "Ambassador animal specialist / animal programs keeper": {
        "title": ["ambassador animal", "animal ambassador", "animal programs keeper", "education keeper", "presentation animals"],
        "tags": ["guest_education", "animal_handling", "public_speaking"],
    },
    "Zoo / aquarium animal trainer": {
        "title": ["animal trainer", "assistant trainer", "senior trainer", "marine mammal trainer", "behavior trainer", "pinniped trainer"],
        "tags": ["training", "animal_behavior"],
    },
    "Zoo behavioral-husbandry specialist": {
        "title": ["behavioral husbandry", "behavioural husbandry", "curator of behavioral husbandry", "animal behavior manager", "behavior manager", "training coordinator"],
        "tags": ["behavior_observation", "training", "enrichment", "welfare_wellbeing", "animal_behavior"],
    },
    "Zoo / aquarium welfare specialist": {
        "title": ["animal welfare", "animal wellbeing", "animal well-being", "animal welfare specialist", "animal wellbeing specialist", "animal well-being specialist", "welfare and behavior", "welfare & behavior", "welfare manager"],
        "tags": ["welfare_wellbeing", "behavior_observation", "animal_behavior"],
    },
    "Enrichment coordinator / specialist": {
        "title": ["enrichment", "enrichment coordinator", "enrichment specialist", "enrichment manager", "behavioral enrichment"],
        "tags": ["enrichment", "training", "behavior_observation"],
    },
    "Zoo / aquarium behavioral researcher": {
        "title": ["behavior research", "behaviour research", "animal behavior researcher", "animal welfare researcher", "applied research coordinator"],
        "tags": ["research", "behavior_observation", "welfare_wellbeing", "data_analysis"],
    },
    "Zoo animal curator": {
        "title": ["animal curator", "curator of animals", "zoo curator", "general curator", "associate curator", "assistant curator"],
        "tags": ["supervision", "leadership", "husbandry"],
    },
    "Animal collection / management specialist": {
        "title": ["collection manager", "animal collection manager", "animal management specialist", "director of animal care", "animal care manager"],
        "tags": ["supervision", "leadership", "husbandry", "recordkeeping"],
    },
    "Zoo research coordinator": {
        "title": ["zoo research coordinator", "research coordinator", "research manager", "conservation research coordinator"],
        "tags": ["research", "project_management", "data_analysis"],
    },
    "Zoo conservation coordinator": {
        "title": ["zoo conservation coordinator", "conservation program coordinator", "conservation programs manager", "field conservation coordinator", "conservation and research coordinator"],
        "tags": ["conservation", "project_management", "fieldwork"],
    },
    "Zoo / aquarium educator": {
        "title": ["zoo educator", "aquarium educator", "education specialist", "education coordinator", "interpretive educator", "school programs coordinator"],
        "tags": ["guest_education", "public_speaking", "conservation"],
    },
    "Zoo registrar / animal records & permits specialist": {
        "title": ["zoo registrar", "animal registrar", "registrar", "animal records coordinator", "wildlife records specialist"],
        "tags": ["recordkeeping", "zims"],
    },
    "Zoo animal nutritionist / nutrition coordinator": {
        "title": ["zoo nutritionist", "animal nutritionist", "nutrition coordinator", "nutrition manager", "commissary coordinator"],
        "tags": ["feeding_nutrition"],
    },
    "Conservation-breeding technician": {
        "title": ["conservation breeding technician", "breeding program technician", "conservation husbandry technician", "conservation keeper"],
        "tags": ["conservation", "husbandry", "recordkeeping"],
    },
    "Conservation-breeding scientist": {
        "title": ["conservation breeding scientist", "reproductive scientist", "reintroduction biologist"],
        "tags": ["conservation", "research", "data_analysis"],
    },
    "Population biologist / zoo population management scientist": {
        "title": ["population biologist", "population management scientist", "population management researcher", "population planning"],
        "tags": ["research", "data_analysis", "conservation"],
    },
    "SSP coordinator / studbook keeper": {
        "title": ["ssp coordinator", "ssp program leader", "studbook keeper", "animal program leader", "species survival plan"],
        "tags": ["recordkeeping", "conservation", "project_management"],
    },
    "Wildlife rehabilitator": {
        "title": ["wildlife rehabilitator", "wildlife rehabilitation specialist", "wildlife care specialist hospital"],
        "tags": ["animal_handling", "veterinary_support", "husbandry"],
    },
    "Sanctuary animal caregiver": {
        "title": ["sanctuary caregiver", "sanctuary animal caregiver", "sanctuary keeper", "animal sanctuary caretaker"],
        "tags": ["husbandry", "feeding_nutrition", "cleaning_sanitation", "animal_handling"],
    },
}

OUT_OF_SCOPE_TERMS = {
    "accountant", "accounting", "admissions", "cashier", "cook", "culinary", "custodian",
    "development officer", "electrician", "facilities", "finance", "food service", "fundraiser",
    "gift shop", "groundskeeper", "guest services", "human resources", "information technology",
    "janitor", "marketing", "membership", "payroll", "retail", "security officer", "web developer",
}
ADJACENT_TERMS = {
    "veterinarian", "veterinary technician", "vet tech", "hospital manager", "horticulturist",
    "horticulture", "landscape", "water quality technician", "life support systems",
}
ANIMAL_SCOPE_TERMS = {
    "animal", "aquarium", "aquarist", "avian", "behavior", "behaviour", "conservation",
    "elephant", "fish", "herpetology", "keeper", "marine mammal", "nutrition", "population",
    "primate", "research", "sanctuary", "ssp", "studbook", "trainer", "welfare", "wellbeing",
    "wildlife", "zoo", "zoological",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def norm(value: str | None) -> str:
    value = (value or "").lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def load_json_list(value: str | None) -> set[str]:
    try:
        parsed = json.loads(value or "[]")
        return {norm(x) for x in parsed if isinstance(x, str)}
    except (TypeError, ValueError, json.JSONDecodeError):
        return set()


def contains_phrase(text: str, phrase: str) -> bool:
    return f" {norm(phrase)} " in f" {norm(text)} "


def ensure_schema(con: sqlite3.Connection) -> None:
    con.executescript((ROOT / "database" / "migration_aza_market_jobs.sql").read_text(encoding="utf-8"))
    con.commit()


def career_lookup(con: sqlite3.Connection) -> tuple[dict[str, str], dict[str, list[tuple[str, str]]]]:
    by_name = {r["name"]: r["career_id"] for r in con.execute("SELECT career_id,name FROM career_roles WHERE active=1")}
    aliases: dict[str, list[tuple[str, str]]] = {}
    for r in con.execute("SELECT career_id,alias,alias_type FROM career_aliases"):
        aliases.setdefault(r["career_id"], []).append((r["alias"], r["alias_type"]))
    return by_name, aliases


def score_roles(row: sqlite3.Row, by_name: dict[str, str], aliases: dict[str, list[tuple[str, str]]]):
    title = norm(row["title"])
    context = norm(" ".join(str(row[k] or "") for k in ("title", "employer", "duties_summary", "requirements_summary", "education_field")))
    blob = context
    duty_tags = load_json_list(row["duty_tags_json"])
    skill_tags = load_json_list(row["skill_tags_json"])
    all_tags = duty_tags | skill_tags
    scores: dict[str, float] = {}
    reasons: dict[str, list[str]] = {}

    def add(cid: str, amount: float, reason: str) -> None:
        scores[cid] = scores.get(cid, 0.0) + amount
        reasons.setdefault(cid, []).append(reason)

    # Curated aliases are strong title evidence, but generic one-word aliases are
    # deliberately weaker than exact or multiword matches.
    for cid, values in aliases.items():
        for alias, alias_type in values:
            a = norm(alias)
            if not a or len(a) < 4:
                continue
            strong = alias_type != "searchable_title"
            if title == a:
                add(cid, 0.94 if strong else 0.72, f'exact curated title/alias: "{alias}"')
                break
            if len(a.split()) >= 2 and contains_phrase(title, a):
                add(cid, 0.68 if strong else 0.55, f'curated title phrase: "{alias}"')
                break

    for role_name, rule in ROLE_RULES.items():
        cid = by_name.get(role_name)
        if not cid:
            continue
        matched = [p for p in rule["title"] if contains_phrase(title, p)]
        if matched:
            longest = max(matched, key=len)
            add(cid, 0.78 if len(norm(longest).split()) >= 2 else 0.62, f'title rule: "{longest}"')
        tag_hits = [t for t in rule["tags"] if norm(t) in all_tags]
        if tag_hits:
            add(cid, min(0.28, 0.07 * len(tag_hits)), "supporting tags: " + ", ".join(tag_hits[:4]))

    # A few generic-title safeguards reduce false positives without hiding them.
    if "veterinary" in blob or "veterinarian" in blob:
        for name in ("Zookeeper / animal-care specialist", "Wildlife rehabilitator"):
            cid = by_name.get(name)
            if cid in scores:
                scores[cid] *= 0.55
                reasons[cid].append("reduced: veterinary context")
    if "education" in title and "animal" not in title:
        cid = by_name.get("Zoo / aquarium educator")
        if cid in scores:
            scores[cid] *= 0.85
    sanctuary_id = by_name.get("Sanctuary animal caregiver")
    if sanctuary_id in scores and "sanctuary" not in context:
        scores[sanctuary_id] *= 0.50
        reasons[sanctuary_id].append("reduced: no sanctuary setting signal")

    ranked = []
    for cid, raw in scores.items():
        score = min(0.99, round(raw, 3))
        if score >= 0.55:
            ranked.append((cid, score, "; ".join(reasons[cid])))
    ranked.sort(key=lambda x: (-x[1], x[0]))
    return ranked


def classify(row: sqlite3.Row, ranked):
    title = norm(row["title"])
    blob = norm(" ".join(str(row[k] or "") for k in ("title", "duties_summary", "requirements_summary")))
    if ranked:
        return "in_scope", ranked[0][1], "One or more conservative canonical-role rules matched."
    if any(contains_phrase(title, term) for term in ADJACENT_TERMS):
        return "adjacent", 0.90, "Clearly animal-sector work, but outside the current career-map scope."
    if any(contains_phrase(title, term) for term in OUT_OF_SCOPE_TERMS) and not any(contains_phrase(blob, term) for term in ANIMAL_SCOPE_TERMS):
        return "out_of_scope", 0.93, "Institutional-support title without a current animal/science scope signal."
    if any(contains_phrase(blob, term) for term in ANIMAL_SCOPE_TERMS):
        return "needs_review", 0.58, "Animal/science scope signal found, but no sufficiently precise role rule matched."
    return "needs_review", 0.35, "Insufficient structured evidence for a safe automatic scope decision."


def review_id(posting_id: str) -> str:
    return "rq_aza_" + hashlib.sha1(posting_id.encode("utf-8")).hexdigest()[:16]


def update_review_queue(con: sqlite3.Connection, posting_id: str, status: str, ranked, reviewed: bool) -> None:
    rid = review_id(posting_id)
    timestamp = now()
    if reviewed or status == "out_of_scope":
        con.execute(
            "UPDATE review_queue SET status=?, reviewed_at=? WHERE review_id=? AND status='open'",
            ("resolved" if reviewed else "not_applicable", timestamp, rid),
        )
        return
    priority = "high" if status == "needs_review" or len(ranked) != 1 else "medium"
    note = "Review AZA scope classification and canonical-role suggestion before website publication."
    con.execute(
        """INSERT INTO review_queue
        (review_id,entity_type,entity_id,issue_type,priority,status,created_at,notes)
        VALUES (?,?,?,?,?,'open',?,?)
        ON CONFLICT(review_id) DO UPDATE SET
          priority=excluded.priority,
          notes=excluded.notes,
          status=CASE WHEN review_queue.status='resolved' THEN review_queue.status ELSE 'open' END""",
        (rid, "market_job_posting", posting_id, "aza_role_match_review", priority, timestamp, note),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB))
    args = ap.parse_args()
    con = sqlite3.connect(Path(args.db))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    ensure_schema(con)
    by_name, aliases = career_lookup(con)

    totals = {"in_scope": 0, "adjacent": 0, "out_of_scope": 0, "needs_review": 0}
    suggestions = 0
    postings = con.execute("SELECT * FROM market_job_postings ORDER BY COALESCE(posted_date,retrieved_at) DESC,posting_id").fetchall()
    for row in postings:
        existing = con.execute("SELECT * FROM market_job_classifications WHERE posting_id=?", (row["posting_id"],)).fetchone()
        if existing and existing["reviewed"]:
            totals[existing["relevance_status"]] = totals.get(existing["relevance_status"], 0) + 1
            update_review_queue(con, row["posting_id"], existing["relevance_status"], [], True)
            continue

        ranked = score_roles(row, by_name, aliases)
        status, confidence, rationale = classify(row, ranked)
        totals[status] += 1
        con.execute(
            """INSERT INTO market_job_classifications
            (posting_id,relevance_status,confidence,method,rationale,reviewed,updated_at)
            VALUES (?,?,?,'rule',?,0,?)
            ON CONFLICT(posting_id) DO UPDATE SET
              relevance_status=excluded.relevance_status,
              confidence=excluded.confidence,
              method='rule',rationale=excluded.rationale,updated_at=excluded.updated_at
            WHERE market_job_classifications.reviewed=0""",
            (row["posting_id"], status, confidence, rationale, now()),
        )
        con.execute("DELETE FROM market_job_role_matches WHERE posting_id=? AND reviewed=0", (row["posting_id"],))
        if status == "in_scope":
            top = ranked[0][1] if ranked else 0
            selected = [x for x in ranked if x[1] >= max(0.55, top - 0.12)][:3]
            for i, (cid, score, reason) in enumerate(selected):
                con.execute(
                    """INSERT INTO market_job_role_matches
                    (posting_id,career_id,match_type,confidence,method,reviewed,review_notes)
                    VALUES (?,?,?,?, 'rule',0,?)
                    ON CONFLICT(posting_id,career_id) DO UPDATE SET
                      match_type=excluded.match_type,confidence=excluded.confidence,
                      method='rule',reviewed=0,review_notes=excluded.review_notes
                    WHERE market_job_role_matches.reviewed=0""",
                    (row["posting_id"], cid, "primary" if i == 0 else "secondary", score, reason),
                )
                suggestions += 1
        update_review_queue(con, row["posting_id"], status, ranked, False)

    con.commit()
    print(f"Classified {len(postings)} AZA postings; created {suggestions} role suggestion(s).")
    print("; ".join(f"{k}={v}" for k, v in totals.items()))
    con.close()


if __name__ == "__main__":
    main()
