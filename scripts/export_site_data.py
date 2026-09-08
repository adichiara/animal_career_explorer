from __future__ import annotations
import json, sqlite3, statistics, csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'database'/'careers.sqlite'
LEGACY=ROOT/'imports'/'legacy_site_data.json'
SEED=ROOT/'imports'/'research_seed_2026-09-08.json'
SITE_DATA=ROOT/'site'/'data.js'
EXPORT_JSON=ROOT/'exports'/'published_data.json'
CAREERS_CSV=ROOT/'exports'/'careers.csv'
POSTINGS_CSV=ROOT/'exports'/'job_postings.csv'
EDGES_CSV=ROOT/'exports'/'career_progression_edges.csv'
SOURCES_CSV=ROOT/'exports'/'sources.csv'
ALIASES_CSV=ROOT/'exports'/'career_aliases.csv'
REVIEW_CSV=ROOT/'exports'/'research_review_queue.csv'

legacy=json.loads(LEGACY.read_text(encoding='utf-8'))
legacy_by={c['name']:c for c in legacy['careers']}

seed=json.loads(SEED.read_text(encoding='utf-8'))
new_by={c['name']:c for c in seed['new_roles']}
DIM_KEYS=seed['dim_keys']

con=sqlite3.connect(DB);con.row_factory=sqlite3.Row

def rows(sql,args=()): return [dict(r) for r in con.execute(sql,args).fetchall()]
def row(sql,args=()):
    r=con.execute(sql,args).fetchone();return dict(r) if r else None

# lookups
families={r['family_id']:r for r in rows('SELECT * FROM role_families')}
domains={r['domain_id']:r for r in rows('SELECT * FROM domains')}
program_db={r['program_id']:r for r in rows('SELECT * FROM programs')}
program_code_by_id={r['program_id']:r['code'] for r in program_db.values()}
sources={r['source_id']:r for r in rows('SELECT * FROM sources')}
comp={r['competency_id']:r for r in rows('SELECT * FROM competencies')}

category_by_domain={
'dm_behavior':'Animal behavior, cognition, welfare & training',
'dm_managed':'Zoos, aquariums, sanctuaries & managed wildlife',
'dm_wildlife':'Wildlife, rehabilitation & conservation',
'dm_organismal':'Organismal biology & ecological science',
'dm_quant':'Quantitative, environmental & agency careers',
'dm_research':'Research, graduate school & academia',
'dm_education':'Education, outreach & science communication',
}

def salary_obs(cid):
    ss=rows('SELECT * FROM salary_observations WHERE career_id=? ORDER BY observation_date DESC',(cid,))
    reviewed_market=rows('''SELECT p.salary_min,p.salary_max,p.salary_unit
        FROM market_job_postings p
        JOIN market_job_role_matches m ON m.posting_id=p.posting_id
        JOIN market_job_classifications c ON c.posting_id=p.posting_id
        WHERE m.career_id=? AND m.reviewed=1 AND c.reviewed=1
          AND c.relevance_status='in_scope' AND p.active_status='active'
          AND p.salary_min IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM job_postings j WHERE j.url=p.source_url)''',(cid,))
    lows=[x['annualized_min'] for x in ss if x['annualized_min'] is not None]
    highs=[x['annualized_max'] for x in ss if x['annualized_max'] is not None]
    def annual(v,unit):
        if v is None:return None
        u=(unit or '').lower()
        if u in ('hour','hourly'):return v*2080
        if u in ('week','weekly'):return v*52
        if u in ('month','monthly'):return v*12
        return v
    for x in reviewed_market:
        lo=annual(x['salary_min'],x['salary_unit']);hi=annual(x['salary_max'] or x['salary_min'],x['salary_unit'])
        if lo is not None:lows.append(lo)
        if hi is not None:highs.append(hi)
    if not lows:return None
    return {'count':len(ss)+len(reviewed_market),'observedMin':round(min(lows)),'observedMax':round(max(highs)) if highs else round(max(lows)),'medianLow':round(statistics.median(lows)),'medianHigh':round(statistics.median(highs)) if highs else round(statistics.median(lows)),'basis':'Current/recent job-posting observations; not a national wage estimate.'}

def source_public(sid):
    s=sources.get(sid)
    if not s:return None
    return {k:s[k] for k in ['source_id','organization','source_type','title','url','published_date','retrieved_date','authority_tier','notes']}

careers=[]
career_name_by_id={}
for r in rows('''SELECT c.*,f.name family_name,f.description family_description,d.domain_id,d.name domain_name,d.description domain_description
                 FROM career_roles c JOIN role_families f ON c.family_id=f.family_id JOIN domains d ON f.domain_id=d.domain_id
                 WHERE c.active=1 ORDER BY c.name'''):
    cid=r['career_id'];career_name_by_id[cid]=r['name']
    base=legacy_by.get(r['name']) or new_by.get(r['name']) or {}
    details=dict(base.get('details') or {})
    details.setdefault('Market status',r.get('market_status') or '')
    details.setdefault('Career type',r.get('role_kind','career').replace('_',' ').title())
    details.setdefault('Typical education / progression',r.get('education_summary') or '')
    # support
    support={}
    for sp in rows('SELECT program_id,support_code,rationale FROM career_program_support WHERE career_id=?',(cid,)):
        support[program_code_by_id[sp['program_id']]]=sp['support_code']
    dims_rows=rows('SELECT dim_key,score FROM career_dimensions WHERE career_id=?',(cid,));dm={x['dim_key']:x['score'] for x in dims_rows};dims=[dm.get(k,0) for k in DIM_KEYS]
    tags=[x['tag'] for x in rows('SELECT tag FROM career_work_tags WHERE career_id=? ORDER BY tag',(cid,))]
    comps=[]
    for x in rows('SELECT competency_id,importance FROM career_competencies WHERE career_id=?',(cid,)):
        cc=comp[x['competency_id']];comps.append({'id':cc['competency_id'],'name':cc['name'],'category':cc['category'],'description':cc['description'],'importance':x['importance']})
    observed=[]
    for x in rows('SELECT * FROM observed_titles WHERE career_id=? ORDER BY observed_date DESC,title',(cid,)):
        observed.append({**x,'source':source_public(x['source_id'])})
    posts=[]
    for x in rows('SELECT * FROM job_postings WHERE career_id=? ORDER BY COALESCE(posted_date,retrieved_date) DESC,title',(cid,)):
        posts.append({**x,'source':source_public(x['source_id'])})
    seen_urls={x.get('url') for x in posts}
    for x in rows('''SELECT p.posting_id,p.title,p.employer,p.location_text location,p.posted_date,
                            p.retrieved_at retrieved_date,p.position_type employment_type,
                            p.education_level_min education_min,p.experience_summary experience_min,
                            p.salary_min,p.salary_max,p.salary_unit,p.currency,p.source_id,
                            p.source_url url,p.active_status,p.requirements_summary notes,
                            m.match_type,m.confidence match_confidence
                     FROM market_job_postings p
                     JOIN market_job_role_matches m ON m.posting_id=p.posting_id
                     JOIN market_job_classifications mc ON mc.posting_id=p.posting_id
                     WHERE m.career_id=? AND m.reviewed=1 AND mc.reviewed=1
                       AND mc.relevance_status='in_scope' AND p.active_status='active'
                     ORDER BY COALESCE(p.posted_date,p.retrieved_at) DESC,p.title''',(cid,)):
        if x['url'] not in seen_urls:
            posts.append({**x,'source':source_public(x['source_id']),'marketSnapshot':True})
            seen_urls.add(x['url'])
    evid=[]
    for x in rows('SELECT * FROM evidence WHERE entity_type="career" AND entity_id=? ORDER BY claim_type',(cid,)):
        evid.append({**x,'source':source_public(x['source_id'])})
    creds=[]
    for x in rows('''SELECT cr.relationship,cr.notes,c.*,s.url source_url,s.retrieved_date source_retrieved
                     FROM career_credentials cr JOIN credentials c ON cr.credential_id=c.credential_id
                     LEFT JOIN sources s ON c.source_id=s.source_id WHERE cr.career_id=?''',(cid,)):
        creds.append(x)
    quals=[]
    for x in rows('''SELECT q.*,s.url source_url,s.title source_title,s.retrieved_date source_retrieved
                     FROM qualification_profiles q JOIN sources s ON q.source_id=s.source_id WHERE q.career_id=?''',(cid,)):
        quals.append(x)
    # maintain broad proxy salary only for legacy; current-market salary stays separate
    entry=base.get('entrySalary');mid=base.get('midSalary')
    aliases=[x['alias'] for x in rows('SELECT alias FROM career_aliases WHERE career_id=? ORDER BY alias_type,alias',(cid,))]
    careers.append({
        'id':cid,'name':r['name'],'slug':r['slug'],'category':base.get('category',category_by_domain.get(r['domain_id'],r['domain_name'])),
        'domain':{'id':r['domain_id'],'name':r['domain_name'],'description':r['domain_description']},
        'roleFamily':{'id':r['family_id'],'name':r['family_name'],'description':r['family_description']},
        'roleKind':r['role_kind'],'marketStatus':r['market_status'],'evidenceStatus':r['evidence_status'],'lastVerified':r['last_verified'],
        'roleFocus':r['description'] or base.get('roleFocus',''),'details':details,'support':support,'notes':base.get('notes',''),
        'dims':dims,'directContact':r['direct_animal_contact'] or base.get('directContact','Low / variable'),
        'educationBand':r['education_summary'] or base.get('educationBand',''),'careerStage':r['career_stage'],'workTags':tags,
        'entrySalary':entry,'midSalary':mid,'observedMarketSalary':salary_obs(cid),'aliases':aliases,
        'competencies':comps,'observedTitles':observed,'recentPostings':posts,'evidence':evid,'credentials':creds,'qualificationProfiles':quals,
    })

# Explicit progression edges
edges=[]
for e in rows('SELECT * FROM career_edges ORDER BY relationship_type,typicality'):
    edges.append({**e,'fromCareer':career_name_by_id.get(e['from_career_id']),'toCareer':career_name_by_id.get(e['to_career_id']),'source':source_public(e['source_id']) if e.get('source_id') else None})

# Programs retain detailed legacy profiles + normalized competency links
programs=[]
legacy_prog={p['code']:p for p in legacy['programs']}
for p in rows('SELECT * FROM programs WHERE active=1 ORDER BY code'):
    b=dict(legacy_prog[p['code']])
    pc=[]
    for x in rows('SELECT competency_id,strength,evidence_note FROM program_competencies WHERE program_id=? ORDER BY strength DESC',(p['program_id'],)):
        cc=comp[x['competency_id']];pc.append({'id':cc['competency_id'],'name':cc['name'],'category':cc['category'],'description':cc['description'],'strength':x['strength'],'evidenceNote':x['evidence_note']})
    b['competencies']=pc;b['lastVerified']=p['last_verified'];programs.append(b)

# Taxonomy objects
roleFamilies=[]
for f in rows('''SELECT f.*,d.name domain_name,d.description domain_description,
                 (SELECT COUNT(*) FROM career_roles c WHERE c.family_id=f.family_id AND c.active=1) role_count
                 FROM role_families f JOIN domains d ON f.domain_id=d.domain_id ORDER BY d.name,f.name'''):
    roleFamilies.append(f)
domainList=[]
for d in rows('SELECT * FROM domains ORDER BY name'):
    d['roleCount']=con.execute('''SELECT COUNT(*) FROM career_roles c JOIN role_families f ON c.family_id=f.family_id WHERE f.domain_id=? AND c.active=1''',(d['domain_id'],)).fetchone()[0]
    d['familyCount']=con.execute('SELECT COUNT(*) FROM role_families WHERE domain_id=?',(d['domain_id'],)).fetchone()[0]
    domainList.append(d)

# summary
summary={
    'asOf':'2026-09-08','canonicalRoles':len(careers),'roleFamilies':len(roleFamilies),'domains':len(domainList),
    'observedTitles':con.execute('SELECT COUNT(*) FROM observed_titles').fetchone()[0],
    'currentRecentPostings':con.execute('''SELECT
        (SELECT COUNT(*) FROM job_postings) +
        (SELECT COUNT(DISTINCT p.posting_id) FROM market_job_postings p
         JOIN market_job_role_matches m ON m.posting_id=p.posting_id
         JOIN market_job_classifications c ON c.posting_id=p.posting_id
         WHERE m.reviewed=1 AND c.reviewed=1 AND c.relevance_status='in_scope'
           AND p.active_status='active'
           AND NOT EXISTS (SELECT 1 FROM job_postings j WHERE j.url=p.source_url))''').fetchone()[0],
    'salaryObservations':con.execute('''SELECT
        (SELECT COUNT(*) FROM salary_observations) +
        (SELECT COUNT(DISTINCT p.posting_id) FROM market_job_postings p
         JOIN market_job_role_matches m ON m.posting_id=p.posting_id
         JOIN market_job_classifications c ON c.posting_id=p.posting_id
         WHERE m.reviewed=1 AND c.reviewed=1 AND c.relevance_status='in_scope'
           AND p.active_status='active' AND p.salary_min IS NOT NULL
           AND NOT EXISTS (SELECT 1 FROM job_postings j WHERE j.url=p.source_url))''').fetchone()[0],
    'sources':con.execute('SELECT COUNT(*) FROM sources').fetchone()[0],
    'searchAliases':con.execute('SELECT COUNT(*) FROM career_aliases').fetchone()[0],
    'openReviewItems':con.execute("SELECT COUNT(*) FROM review_queue WHERE status='open'").fetchone()[0],
    'explicitProgressionEdges':len(edges),'competencies':len(comp),
    'rolesWithPostingEvidence':con.execute('''SELECT COUNT(DISTINCT career_id) FROM (
        SELECT career_id FROM job_postings
        UNION
        SELECT m.career_id FROM market_job_role_matches m
        JOIN market_job_postings p ON p.posting_id=m.posting_id
        JOIN market_job_classifications c ON c.posting_id=m.posting_id
        WHERE m.reviewed=1 AND c.reviewed=1 AND c.relevance_status='in_scope' AND p.active_status='active'
    )''').fetchone()[0],
    'rolesWithObservedTitles':con.execute('SELECT COUNT(DISTINCT career_id) FROM observed_titles').fetchone()[0],
    'sourceTierCounts':{r['authority_tier']:r['n'] for r in rows('SELECT authority_tier,COUNT(*) n FROM sources GROUP BY authority_tier')},
    'marketSnapshotJobs':con.execute('SELECT COUNT(*) FROM market_job_postings').fetchone()[0],
    'marketJobsClassified':con.execute('SELECT COUNT(*) FROM market_job_classifications').fetchone()[0],
    'marketJobsReviewed':con.execute('SELECT COUNT(*) FROM market_job_classifications WHERE reviewed=1').fetchone()[0],
    'marketJobsMatched':con.execute("SELECT COUNT(DISTINCT posting_id) FROM market_job_role_matches WHERE reviewed=1").fetchone()[0],
    'marketJobsPendingReview':con.execute("SELECT COUNT(*) FROM market_job_classifications WHERE reviewed=0 AND relevance_status IN ('in_scope','adjacent','needs_review')").fetchone()[0],
    'marketScrapeDate':con.execute("SELECT MAX(completed_at) FROM market_job_scrape_runs WHERE status LIKE 'completed%'").fetchone()[0],
}

out={k:v for k,v in legacy.items() if k not in ['careers','programs']}
out['programs']=programs;out['careers']=careers
out['domains']=domainList;out['roleFamilies']=roleFamilies;out['careerEdges']=edges;out['sources']=list(sources.values());out['dataSummary']=summary
out['researchGaps']=rows("""SELECT q.review_id,q.entity_id,c.name career_name,q.issue_type,q.priority,q.status,q.created_at,q.notes FROM review_queue q LEFT JOIN career_roles c ON q.entity_type='career' AND q.entity_id=c.career_id WHERE q.status='open' ORDER BY CASE q.priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,c.name""")
out['evidenceStatusLabels']={
'verified_current_market':'Current/recent market evidence','verified_occupation_or_title':'Verified occupation/title','verified_function_title_varies':'Verified work; title varies','established_scientific_specialty':'Established scientific specialty','verified_professional_role':'Verified professional role','verified_professional_assignment':'Professional assignment / additional responsibility'}
out['roleKindLabels']={'career':'Career role','scientific_specialty':'Scientific specialty','professional_assignment':'Professional assignment','later_career':'Later-career role','education_path':'Graduate education pathway'}

EXPORT_JSON.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
SITE_DATA.write_text('window.EXPLORER_DATA = '+json.dumps(out,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')

# Human-review exports
def write_csv(path,table):
    rr=rows(f'SELECT * FROM {table}')
    if not rr:return
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rr[0].keys()));w.writeheader();w.writerows(rr)
write_csv(CAREERS_CSV,'career_roles');write_csv(POSTINGS_CSV,'job_postings');write_csv(EDGES_CSV,'career_edges');write_csv(SOURCES_CSV,'sources');write_csv(ALIASES_CSV,'career_aliases');write_csv(REVIEW_CSV,'review_queue')
print(SITE_DATA)
print('roles',len(careers),'families',len(roleFamilies),'postings',summary['currentRecentPostings'])
