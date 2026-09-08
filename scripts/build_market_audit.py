from __future__ import annotations
import sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'database'/'careers.sqlite';OUT=ROOT/'reports'/'market_content_audit.md'
con=sqlite3.connect(DB);con.row_factory=sqlite3.Row
q=lambda s,a=():con.execute(s,a).fetchall()
lines=['# Animal Career Market Content Audit','', '**Research snapshot:** 2026-09-08','',
'This audit describes the evidence currently loaded into the career-exploration database. It is a coverage report, not a claim that the labor market is exhausted by the listed roles or postings.','']
lines += ['## Scope expansion','',
'Legacy prototype: **73** career/pathway records. Current normalized database: **93** canonical roles/pathways organized into **32** role families and **7** domains. The expansion is within the established scope: behavior/welfare, managed-animal work, wildlife/rehabilitation/conservation, organismal science, quantitative/environmental work, research, and related education/communication.','']
market_total=con.execute('SELECT COUNT(*) FROM market_job_postings').fetchone()[0]
market_reviewed=con.execute('SELECT COUNT(*) FROM market_job_classifications WHERE reviewed=1').fetchone()[0]
market_matched=con.execute('SELECT COUNT(DISTINCT posting_id) FROM market_job_role_matches WHERE reviewed=1').fetchone()[0]
lines += ['## AZA complete-board layer','',
f'- Board listings captured: **{market_total}**',
f'- Human-reviewed scope classifications: **{market_reviewed}**',
f'- Accepted reviewed role matches: **{market_matched}**','',
'Complete-board listings are stored independently from the canonical career taxonomy. Only reviewed, in-scope matches contribute to website career evidence.','']
for r in q('SELECT relevance_status,reviewed,COUNT(*) n FROM market_job_classifications GROUP BY relevance_status,reviewed ORDER BY relevance_status,reviewed'):
    lines.append(f"- {r['relevance_status']} ({'reviewed' if r['reviewed'] else 'awaiting review'}): **{r['n']}**")
if market_total: lines.append('')
lines += ['## Domain coverage','']
for d in q('SELECT * FROM domains ORDER BY name'):
    rc=con.execute('''SELECT COUNT(*) FROM career_roles c JOIN role_families f ON c.family_id=f.family_id WHERE f.domain_id=?''',(d['domain_id'],)).fetchone()[0]
    pc=con.execute('''SELECT COUNT(*) FROM job_postings j JOIN career_roles c ON j.career_id=c.career_id JOIN role_families f ON c.family_id=f.family_id WHERE f.domain_id=?''',(d['domain_id'],)).fetchone()[0]
    oc=con.execute('''SELECT COUNT(*) FROM observed_titles o JOIN career_roles c ON o.career_id=c.career_id JOIN role_families f ON c.family_id=f.family_id WHERE f.domain_id=?''',(d['domain_id'],)).fetchone()[0]
    lines += [f"### {d['name']}",f"{d['description']}",'',f'- Canonical roles: **{rc}**',f'- Directly observed titles: **{oc}**',f'- Current/recent posting observations: **{pc}**','']
    fams=q('SELECT * FROM role_families WHERE domain_id=? ORDER BY name',(d['domain_id'],))
    for f in fams:
        roles=[r['name'] for r in q('SELECT name FROM career_roles WHERE family_id=? ORDER BY name',(f['family_id'],))]
        lines.append(f"- **{f['name']}** ({len(roles)}): "+'; '.join(roles))
    lines.append('')
lines += ['## Examples of directly observed employer/professional titles','']
for d in q('SELECT * FROM domains ORDER BY name'):
    obs=q('''SELECT o.title,o.organization,o.location,o.observed_date,c.name canonical FROM observed_titles o JOIN career_roles c ON o.career_id=c.career_id JOIN role_families f ON c.family_id=f.family_id WHERE f.domain_id=? ORDER BY COALESCE(o.observed_date,'') DESC,o.title LIMIT 18''',(d['domain_id'],))
    if not obs:continue
    lines += [f"### {d['name']}",'']
    for r in obs:lines.append(f"- **{r['title']}** — {r['organization'] or 'professional source'}{(' — '+r['location']) if r['location'] else ''} → canonical role: *{r['canonical']}*")
    lines.append('')
lines += ['## Posting-level salary observations','',
'Posting salaries remain separate from O*NET/BLS occupation benchmarks. They are examples of specific jobs at specific employers and locations, not universal salary ranges.','']
for r in q('''SELECT c.name,COUNT(s.salary_id) n,MIN(s.annualized_min) lo,MAX(s.annualized_max) hi FROM salary_observations s JOIN career_roles c ON s.career_id=c.career_id GROUP BY c.career_id ORDER BY c.name'''):
    lines.append(f"- **{r['name']}** — {r['n']} observation(s); annualized observed span **${r['lo']:,.0f}–${r['hi']:,.0f}**")
lines.append('')
lines += ['## Formal qualification and credential evidence','']
for r in q('''SELECT c.name,q.organization,q.series_code,q.name qname,q.education_requirement,q.coursework_requirement,q.experience_requirement,s.url FROM qualification_profiles q JOIN career_roles c ON q.career_id=c.career_id JOIN sources s ON q.source_id=s.source_id ORDER BY c.name'''):
    lines += [f"### {r['name']} — {r['qname']}",f"- Organization: {r['organization']}",f"- Education: {r['education_requirement'] or '—'}",f"- Coursework: {r['coursework_requirement'] or '—'}",f"- Experience: {r['experience_requirement'] or '—'}",f"- Source: {r['url']}",'']
for r in q('''SELECT cr.name career,c.name credential,c.organization,cc.relationship,cc.notes,s.url FROM career_credentials cc JOIN career_roles cr ON cc.career_id=cr.career_id JOIN credentials c ON cc.credential_id=c.credential_id LEFT JOIN sources s ON c.source_id=s.source_id ORDER BY cr.name,c.name'''):
    lines.append(f"- **{r['career']}** — {r['credential']} ({r['relationship']}); {r['notes'] or ''} Source: {r['url'] or '—'}")
lines += ['','## Progression evidence','',
'The database contains explicit progression edges as a separate layer from similarity-based suggestions in the website.','']
for typ,n in [(r['relationship_type'],r['n']) for r in q('SELECT relationship_type,COUNT(*) n FROM career_edges GROUP BY relationship_type ORDER BY relationship_type')]:lines.append(f'- {typ.replace("_"," ")}: **{n}**')
lines.append('')
for r in q('''SELECT a.name frm,b.name too,e.relationship_type,e.typicality,e.education_change,e.experience_change,e.evidence_status,e.notes FROM career_edges e JOIN career_roles a ON e.from_career_id=a.career_id JOIN career_roles b ON e.to_career_id=b.career_id WHERE e.evidence_status='verified' ORDER BY a.name,b.name LIMIT 30'''):
    lines.append(f"- **{r['frm']} → {r['too']}** — {r['relationship_type'].replace('_',' ')}, {r['typicality']}; education: {r['education_change'] or '—'}; experience: {r['experience_change'] or '—'}. {r['notes'] or ''}")
lines += ['','## Known research gaps','',
'Gaps are stored in the managed review queue rather than hidden.','']
for r in q("SELECT issue_type,priority,COUNT(*) n FROM review_queue WHERE status='open' GROUP BY issue_type,priority ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,issue_type"):
    lines.append(f"- **{r['priority']} — {r['issue_type']}**: {r['n']} open items")
lines += ['','## Source registry','']
for r in q('SELECT * FROM sources ORDER BY authority_tier,organization,title'):
    lines.append(f"- **Tier {r['authority_tier']} — {r['organization']}** — {r['title']} ({r['source_type']}); retrieved {r['retrieved_date']}; {r['url']}")
OUT.write_text('\n'.join(lines),encoding='utf-8');print(OUT)
