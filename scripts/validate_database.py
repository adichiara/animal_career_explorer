from __future__ import annotations
import sqlite3, csv, json
from pathlib import Path
from datetime import date, datetime

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'database'/'careers.sqlite'
REPORT=ROOT/'reports'/'validation_report.md'
CSV=ROOT/'exports'/'career_evidence_coverage.csv'
TODAY=date(2026,9,8)

con=sqlite3.connect(DB)
con.row_factory=sqlite3.Row
errors=[]; warnings=[]

fk=con.execute('PRAGMA foreign_key_check').fetchall()
if fk: errors.append(f'{len(fk)} foreign-key violations')

# Required relationship completeness
roles=con.execute('SELECT * FROM career_roles WHERE active=1 ORDER BY name').fetchall()
programs=con.execute('SELECT * FROM programs WHERE active=1').fetchall()
for r in roles:
    dims=con.execute('SELECT COUNT(*) n FROM career_dimensions WHERE career_id=?',(r['career_id'],)).fetchone()['n']
    if dims!=10: errors.append(f"{r['name']}: expected 10 dimensions, found {dims}")
    supp=con.execute('SELECT COUNT(*) n FROM career_program_support WHERE career_id=?',(r['career_id'],)).fetchone()['n']
    if supp!=len(programs): warnings.append(f"{r['name']}: program-support rows {supp}/{len(programs)}")
    tags=con.execute('SELECT COUNT(*) n FROM career_work_tags WHERE career_id=?',(r['career_id'],)).fetchone()['n']
    if tags==0: warnings.append(f"{r['name']}: no work tags")

# Orphan/quality checks
for row in con.execute("SELECT posting_id,title FROM job_postings WHERE source_id IS NULL OR url IS NULL OR url='' "):
    errors.append(f"Posting missing source/url: {row['posting_id']} {row['title']}")
for row in con.execute("SELECT edge_id FROM career_edges WHERE from_career_id=to_career_id"):
    errors.append(f"Self-referencing progression edge: {row['edge_id']}")
for row in con.execute("SELECT source_id,url FROM sources WHERE url NOT LIKE 'http%'"):
    warnings.append(f"Source URL not HTTP(S): {row['source_id']} {row['url']}")
for row in con.execute("SELECT posting_id,confidence FROM market_job_role_matches WHERE confidence<0 OR confidence>1"):
    errors.append(f"Market role-match confidence outside 0–1: {row['posting_id']} {row['confidence']}")
for row in con.execute("SELECT posting_id,match_type FROM market_job_role_matches WHERE match_type NOT IN ('primary','secondary','adjacent')"):
    errors.append(f"Invalid market role-match type: {row['posting_id']} {row['match_type']}")
for row in con.execute("SELECT posting_id,relevance_status FROM market_job_classifications WHERE relevance_status NOT IN ('in_scope','adjacent','out_of_scope','needs_review')"):
    errors.append(f"Invalid market relevance status: {row['posting_id']} {row['relevance_status']}")
for row in con.execute('''SELECT m.posting_id FROM market_job_role_matches m
                          LEFT JOIN market_job_classifications c ON c.posting_id=m.posting_id
                          WHERE m.reviewed=1 AND COALESCE(c.reviewed,0)=0'''):
    errors.append(f"Reviewed market match lacks reviewed classification: {row['posting_id']}")
for row in con.execute('''SELECT c.posting_id FROM market_job_classifications c
                          WHERE c.reviewed=1 AND c.relevance_status='in_scope'
                          AND NOT EXISTS (SELECT 1 FROM market_job_role_matches m
                                          WHERE m.posting_id=c.posting_id AND m.reviewed=1
                                            AND m.match_type='primary')'''):
    errors.append(f"Reviewed in-scope market job lacks primary role match: {row['posting_id']}")

# Coverage metrics
summary={}
for t in ['domains','role_families','career_roles','career_aliases','observed_titles','job_postings','salary_observations','competencies','credentials','qualification_profiles','career_edges','sources','evidence','review_queue','ingest_batches','change_log','market_job_postings','market_job_classifications','market_job_role_matches','market_job_scrape_runs']:
    summary[t]=con.execute(f'SELECT COUNT(*) n FROM {t}').fetchone()['n']

statuses=con.execute('SELECT evidence_status,COUNT(*) n FROM career_roles WHERE active=1 GROUP BY evidence_status ORDER BY n DESC').fetchall()
source_tiers=con.execute('SELECT authority_tier,COUNT(*) n FROM sources GROUP BY authority_tier ORDER BY authority_tier').fetchall()
source_types=con.execute('SELECT source_type,COUNT(*) n FROM sources GROUP BY source_type ORDER BY n DESC').fetchall()

coverage=[]
for r in roles:
    cid=r['career_id']
    obs=con.execute('SELECT COUNT(*) n FROM observed_titles WHERE career_id=?',(cid,)).fetchone()['n']
    posts=con.execute('''SELECT COUNT(*) n FROM (
        SELECT url FROM job_postings WHERE career_id=?
        UNION
        SELECT p.source_url FROM market_job_postings p
        JOIN market_job_role_matches m ON m.posting_id=p.posting_id
        JOIN market_job_classifications mc ON mc.posting_id=p.posting_id
        WHERE m.career_id=? AND m.reviewed=1 AND mc.reviewed=1
          AND mc.relevance_status='in_scope' AND p.active_status='active'
    )''',(cid,cid)).fetchone()['n']
    salaries=con.execute('''SELECT
        (SELECT COUNT(*) FROM salary_observations WHERE career_id=?) +
        (SELECT COUNT(DISTINCT p.posting_id) FROM market_job_postings p
         JOIN market_job_role_matches m ON m.posting_id=p.posting_id
         JOIN market_job_classifications mc ON mc.posting_id=p.posting_id
         WHERE m.career_id=? AND m.reviewed=1 AND mc.reviewed=1
           AND mc.relevance_status='in_scope' AND p.active_status='active'
           AND p.salary_min IS NOT NULL) n''',(cid,cid)).fetchone()['n']
    evid=con.execute('SELECT COUNT(*) n FROM evidence WHERE entity_type="career" AND entity_id=?',(cid,)).fetchone()['n']
    creds=con.execute('SELECT COUNT(*) n FROM career_credentials WHERE career_id=?',(cid,)).fetchone()['n']
    quals=con.execute('SELECT COUNT(*) n FROM qualification_profiles WHERE career_id=?',(cid,)).fetchone()['n']
    edgesout=con.execute('SELECT COUNT(*) n FROM career_edges WHERE from_career_id=?',(cid,)).fetchone()['n']
    edgesin=con.execute('SELECT COUNT(*) n FROM career_edges WHERE to_career_id=?',(cid,)).fetchone()['n']
    coverage.append(dict(career_id=cid,name=r['name'],evidence_status=r['evidence_status'],role_kind=r['role_kind'],last_verified=r['last_verified'],observed_titles=obs,current_recent_postings=posts,salary_observations=salaries,explicit_evidence=evid,credentials=creds,qualification_profiles=quals,progression_edges_out=edgesout,progression_edges_in=edgesin))

with open(CSV,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(coverage[0].keys()));w.writeheader();w.writerows(coverage)

current_roles=sum(1 for x in coverage if x['current_recent_postings']>0)
observed_roles=sum(1 for x in coverage if x['observed_titles']>0)
explicit_roles=sum(1 for x in coverage if x['explicit_evidence']>0)
edge_roles=sum(1 for x in coverage if x['progression_edges_out']+x['progression_edges_in']>0)
open_review_items=con.execute("SELECT COUNT(*) FROM review_queue WHERE status='open'").fetchone()[0]

# Freshness
fresh=[]; stale=[]
for s in con.execute('SELECT source_id,organization,title,retrieved_date,url FROM sources ORDER BY organization,title'):
    try:
        dt=datetime.strptime(s['retrieved_date'],'%Y-%m-%d').date(); age=(TODAY-dt).days
    except Exception: age=None
    (fresh if age is not None and age<=365 else stale).append((s,age))

lines=[]
lines += ['# Animal Career Data Project — Validation Report','',f'**Validation date:** {TODAY.isoformat()}','',
          '## Result','',f"- **Errors:** {len(errors)}",f"- **Warnings:** {len(warnings)}",f"- **Foreign-key violations:** {len(fk)}",'']
if errors:
    lines += ['### Errors','']+[f'- {e}' for e in errors]+['']
if warnings:
    lines += ['### Warnings','']+[f'- {w}' for w in warnings[:100]]+(['- … additional warnings omitted from report display' ] if len(warnings)>100 else [])+['']
lines += ['## Database scope','',
          f"- Domains: **{summary['domains']}**",
          f"- Role families: **{summary['role_families']}**",
          f"- Canonical career roles/pathways: **{summary['career_roles']}**",
          f"- Curated search aliases: **{summary['career_aliases']}**",
          f"- Observed market titles: **{summary['observed_titles']}**",
          f"- Current/recent job-posting observations: **{summary['job_postings']}**",
          f"- Salary observations from postings: **{summary['salary_observations']}**",
          f"- Competencies: **{summary['competencies']}**",
          f"- Credentials: **{summary['credentials']}**",
          f"- Formal qualification profiles: **{summary['qualification_profiles']}**",
          f"- Explicit career-progression edges: **{summary['career_edges']}**",
          f"- Registered sources: **{summary['sources']}**",
          f"- Explicit evidence claims: **{summary['evidence']}**",
          f"- Open research-review items: **{open_review_items}**",
          f"- Ingest batches recorded: **{summary['ingest_batches']}**",
          f"- Change-log entries: **{summary['change_log']}**",'']
lines += ['## AZA complete-board ingestion','',
          f"- Market-board postings captured: **{summary['market_job_postings']}**",
          f"- Scope classifications: **{summary['market_job_classifications']}**",
          f"- Proposed/reviewed canonical-role links: **{summary['market_job_role_matches']}**",
          f"- Human-reviewed classifications: **{con.execute('SELECT COUNT(*) FROM market_job_classifications WHERE reviewed=1').fetchone()[0]}**",
          f"- Accepted reviewed job-to-role links: **{con.execute('SELECT COUNT(*) FROM market_job_role_matches WHERE reviewed=1').fetchone()[0]}**",
          f"- Scrape runs recorded: **{summary['market_job_scrape_runs']}**",'',
          'Complete-board listings remain separate from curated career evidence. Only reviewed, in-scope role matches are published into career profiles.','']
lines += ['## Evidence coverage','',
          f'- Roles with at least one observed title: **{observed_roles}/{len(coverage)}**',
          f'- Roles with a current/recent posting in this research snapshot: **{current_roles}/{len(coverage)}**',
          f'- Roles with an explicit evidence claim: **{explicit_roles}/{len(coverage)}**',
          f'- Roles connected to at least one explicit progression edge: **{edge_roles}/{len(coverage)}**','',
          'A role without a current posting is **not** treated as nonexistent. Current postings are observations of the labor market at one point in time; role existence can also be supported by professional organizations, employer staff directories, federal occupational series, and established scientific specialties.','']
lines += ['### Career evidence-status distribution','']+[f"- {r['evidence_status']}: **{r['n']}**" for r in statuses]+['']
lines += ['### Source authority tiers','']+[f"- Tier {r['authority_tier']}: **{r['n']}** sources" for r in source_tiers]+['', '### Source types','']+[f"- {r['source_type']}: **{r['n']}**" for r in source_types]+['']
lines += ['## Freshness','',f'- Sources retrieved within the last 365 days: **{len(fresh)}/{len(fresh)+len(stale)}**',f'- Sources older than 365 days or with unparseable retrieval date: **{len(stale)}**','']
lines += ['## Important interpretation rules','',
          '- **Canonical role ≠ employer title.** Canonical roles organize the exploration experience; observed titles preserve what employers/professional organizations actually call the work.',
          '- **Job postings are observations, not the definition of a field.** They are used to validate titles, qualifications, duties, salary ranges, and progression patterns.',
          '- **O*NET/BLS data remain broad benchmarks.** Niche animal-care, welfare, zoo, rehabilitation, and conservation roles use posting-level and professional-organization evidence when a dedicated occupation code does not exist.',
          '- **Program support is analytical.** S/C/G/N support mappings summarize curriculum fit and should be periodically revalidated as curricula change.',
          '- **Progression edges are not guaranteed promotions.** They represent observed or professionally plausible transitions; edge-level evidence status distinguishes stronger from more inferential relationships.','']
lines += ['## Managed research-review queue','',
          'Known evidence gaps are materialized in the database rather than hidden. The current open queue contains:',
          *[f"- {r['issue_type']} ({r['priority']} priority): **{r['n']}**" for r in con.execute("SELECT issue_type,priority,COUNT(*) n FROM review_queue WHERE status='open' GROUP BY issue_type,priority ORDER BY priority,issue_type")],
          '',
          '## Review priorities for the next research cycle','',
          '1. Expand posting observations for career families with few or no current examples, especially shelter behavior, sanctuary work, cognition research, and conservation-breeding/population roles.',
          '2. Add posting-specific education and experience fields where source pages provide them.',
          '3. Expand salary observations so niche roles rely less on broad occupation proxies.',
          '4. Add more explicit source-backed progression edges from real job ladders and employer classifications.',
          '5. Revalidate all ten undergraduate program competency mappings against 2027–2028 catalogs before application decisions.','',
          f'Full row-level evidence coverage is exported to `{CSV.name}`.','']
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print(REPORT)
print(CSV)
print('errors',len(errors),'warnings',len(warnings))
if errors: raise SystemExit(1)
