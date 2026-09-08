#!/usr/bin/env python3
import csv, json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'database' / 'careers.sqlite'
OUT = ROOT / 'exports' / 'aza_market_jobs.csv'

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
rows = con.execute('''SELECT p.source_external_id AS aza_job_id,p.title,p.employer,p.location_text,p.posted_date,
closing_date,anticipated_start_date,aza_member,position_type,employment_status,
salary_min,salary_max,salary_unit,currency,education_level_min,education_field,
experience_years_min,duties_summary,requirements_summary,duty_tags_json,skill_tags_json,
credential_tags_json,schedule_tags_json,detail_status,active_status,source_url,retrieved_at,last_seen_at,
c.relevance_status,c.confidence AS classification_confidence,c.method AS classification_method,
c.reviewed AS classification_reviewed,
GROUP_CONCAT(cr.name || ' [' || m.match_type || '; ' || ROUND(m.confidence,2) || ']', '; ') AS canonical_role_matches
FROM market_job_postings p
LEFT JOIN market_job_classifications c ON c.posting_id=p.posting_id
LEFT JOIN market_job_role_matches m ON m.posting_id=p.posting_id
LEFT JOIN career_roles cr ON cr.career_id=m.career_id
WHERE p.source_id='source_aza_jobs_board'
GROUP BY p.posting_id
ORDER BY p.posted_date DESC, p.source_external_id DESC''').fetchall()
OUT.parent.mkdir(exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(rows[0].keys() if rows else [
        'aza_job_id','title','employer','location_text','posted_date','closing_date',
        'anticipated_start_date','aza_member','position_type','employment_status','salary_min',
        'salary_max','salary_unit','currency','education_level_min','education_field',
        'experience_years_min','duties_summary','requirements_summary','duty_tags_json',
        'skill_tags_json','credential_tags_json','schedule_tags_json','detail_status','active_status',
        'source_url','retrieved_at','last_seen_at','relevance_status','classification_confidence',
        'classification_method','classification_reviewed','canonical_role_matches'])
    for r in rows: w.writerow([r[k] for k in r.keys()])
print(f'Wrote {len(rows)} rows to {OUT}')
