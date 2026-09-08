#!/usr/bin/env python3
"""Export AZA match suggestions for review or import completed decisions."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "careers.sqlite"
DEFAULT_CSV = ROOT / "exports" / "aza_job_match_review.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def review_id(posting_id: str) -> str:
    return "rq_aza_" + hashlib.sha1(posting_id.encode("utf-8")).hexdigest()[:16]


def safe_json(value: str | None) -> str:
    try:
        return ", ".join(json.loads(value or "[]"))
    except (TypeError, ValueError, json.JSONDecodeError):
        return value or ""


def export_review(con: sqlite3.Connection, path: Path) -> None:
    con.row_factory = sqlite3.Row
    career_names = {r["career_id"]: r["name"] for r in con.execute("SELECT career_id,name FROM career_roles")}
    out = []
    for p in con.execute(
        """SELECT p.*,c.relevance_status,c.confidence classification_confidence,
                  c.rationale classification_rationale,c.reviewed classification_reviewed
           FROM market_job_postings p
           LEFT JOIN market_job_classifications c ON c.posting_id=p.posting_id
           ORDER BY CASE COALESCE(c.relevance_status,'needs_review')
                    WHEN 'needs_review' THEN 1 WHEN 'in_scope' THEN 2
                    WHEN 'adjacent' THEN 3 ELSE 4 END,
                    COALESCE(p.posted_date,p.retrieved_at) DESC,p.title"""
    ):
        matches = con.execute(
            """SELECT career_id,match_type,confidence,review_notes,reviewed
               FROM market_job_role_matches WHERE posting_id=?
               ORDER BY CASE match_type WHEN 'primary' THEN 1 WHEN 'secondary' THEN 2 ELSE 3 END,
                        confidence DESC""",
            (p["posting_id"],),
        ).fetchall()
        primary = next((m for m in matches if m["match_type"] == "primary"), None)
        secondary = [m for m in matches if m["match_type"] != "primary"]
        out.append({
            "posting_id": p["posting_id"],
            "aza_job_id": p["source_external_id"],
            "title": p["title"],
            "employer": p["employer"],
            "location": p["location_text"],
            "posted_date": p["posted_date"],
            "detail_status": p["detail_status"],
            "proposed_relevance": p["relevance_status"] or "needs_review",
            "classification_confidence": p["classification_confidence"],
            "classification_rationale": p["classification_rationale"],
            "suggested_primary_career_id": primary["career_id"] if primary else "",
            "suggested_primary_career": career_names.get(primary["career_id"], "") if primary else "",
            "primary_match_confidence": primary["confidence"] if primary else "",
            "primary_match_rationale": primary["review_notes"] if primary else "",
            "suggested_secondary_career_ids": ";".join(m["career_id"] for m in secondary),
            "suggested_secondary_careers": "; ".join(career_names.get(m["career_id"], m["career_id"]) for m in secondary),
            "education_min": p["education_level_min"],
            "education_field": p["education_field"],
            "experience_years_min": p["experience_years_min"],
            "salary_min": p["salary_min"],
            "salary_max": p["salary_max"],
            "salary_unit": p["salary_unit"],
            "duty_tags": safe_json(p["duty_tags_json"]),
            "skill_tags": safe_json(p["skill_tags_json"]),
            "source_url": p["source_url"],
            "review_decision": "",
            "reviewed_primary_career_id": "",
            "reviewed_secondary_career_ids": "",
            "reviewer_notes": "",
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(out[0]) if out else [
        "posting_id", "aza_job_id", "title", "employer", "location", "posted_date",
        "detail_status", "proposed_relevance", "review_decision", "reviewed_primary_career_id",
        "reviewed_secondary_career_ids", "reviewer_notes",
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out)
    print(f"Wrote {len(out)} review row(s) to {path}")


def parse_ids(value: str) -> list[str]:
    return [x.strip() for x in (value or "").replace(",", ";").split(";") if x.strip()]


def import_review(con: sqlite3.Connection, path: Path) -> None:
    valid_careers = {r[0] for r in con.execute("SELECT career_id FROM career_roles WHERE active=1")}
    valid_decisions = {"accept", "in_scope", "adjacent", "out_of_scope", "needs_review"}
    applied = 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            decision = (row.get("review_decision") or "").strip().lower()
            if not decision:
                continue
            if decision not in valid_decisions:
                raise SystemExit(f"Invalid review_decision {decision!r} for {row.get('posting_id')}")
            posting_id = (row.get("posting_id") or "").strip()
            if not con.execute("SELECT 1 FROM market_job_postings WHERE posting_id=?", (posting_id,)).fetchone():
                raise SystemExit(f"Unknown posting_id: {posting_id}")

            proposed_primary = (row.get("suggested_primary_career_id") or "").strip()
            reviewed_primary = (row.get("reviewed_primary_career_id") or "").strip()
            primary = reviewed_primary or proposed_primary
            proposed_secondary = parse_ids(row.get("suggested_secondary_career_ids") or "")
            reviewed_secondary_raw = row.get("reviewed_secondary_career_ids") or ""
            secondary = parse_ids(reviewed_secondary_raw) if reviewed_secondary_raw.strip() else proposed_secondary
            role_ids = ([primary] if primary else []) + [x for x in secondary if x != primary]
            unknown = [x for x in role_ids if x not in valid_careers]
            if unknown:
                raise SystemExit(f"Unknown career id(s) for {posting_id}: {', '.join(unknown)}")

            status = "in_scope" if decision in {"accept", "in_scope"} else decision
            if status == "in_scope" and not primary:
                raise SystemExit(f"An in-scope decision requires a primary career id: {posting_id}")
            notes = (row.get("reviewer_notes") or "").strip() or "Human review of AZA role-match proposal."
            timestamp = now()
            con.execute(
                """INSERT INTO market_job_classifications
                (posting_id,relevance_status,confidence,method,rationale,reviewed,reviewed_at,updated_at)
                VALUES (?,?,1.0,'reviewed',?,1,?,?)
                ON CONFLICT(posting_id) DO UPDATE SET
                  relevance_status=excluded.relevance_status,confidence=1.0,method='reviewed',
                  rationale=excluded.rationale,reviewed=1,reviewed_at=excluded.reviewed_at,
                  updated_at=excluded.updated_at""",
                (posting_id, status, notes, timestamp, timestamp),
            )
            con.execute("DELETE FROM market_job_role_matches WHERE posting_id=?", (posting_id,))
            if status == "in_scope":
                for i, cid in enumerate(role_ids):
                    con.execute(
                        """INSERT INTO market_job_role_matches
                        (posting_id,career_id,match_type,confidence,method,reviewed,review_notes)
                        VALUES (?,?,?,?, 'reviewed',1,?)""",
                        (posting_id, cid, "primary" if i == 0 else "secondary", 1.0 if i == 0 else 0.9, notes),
                    )
            con.execute(
                "UPDATE review_queue SET status='resolved',reviewed_at=?,notes=? WHERE review_id=?",
                (timestamp, notes, review_id(posting_id)),
            )
            applied += 1
    con.commit()
    print(f"Imported {applied} reviewed decision(s) from {path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB))
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    ap.add_argument("--import-reviewed", action="store_true")
    args = ap.parse_args()
    con = sqlite3.connect(Path(args.db))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript((ROOT / "database" / "migration_aza_market_jobs.sql").read_text(encoding="utf-8"))
    if args.import_reviewed:
        import_review(con, Path(args.csv))
    else:
        export_review(con, Path(args.csv))
    con.close()


if __name__ == "__main__":
    main()
