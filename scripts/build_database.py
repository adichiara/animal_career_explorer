from __future__ import annotations
import json, sqlite3, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEGACY=ROOT/'imports'/'legacy_site_data.json'
SEED=ROOT/'imports'/'research_seed_2026-09-08.json'
SCHEMA=ROOT/'database'/'schema.sql'
DB=ROOT/'database'/'careers.sqlite'

legacy=json.loads(LEGACY.read_text(encoding='utf-8'))
seed=json.loads(SEED.read_text(encoding='utf-8'))
TODAY=seed['dataset_date']
DIM_KEYS=seed['dim_keys']
MARKET_TABLES=['market_job_postings','market_job_classifications','market_job_scrape_runs','market_job_role_matches']

def snapshot_market_data():
    """Keep the independently collected AZA snapshot across canonical rebuilds."""
    if not DB.exists(): return {'source':None,'tables':{}}
    old=sqlite3.connect(DB);old.row_factory=sqlite3.Row
    present={r['name'] for r in old.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    source=dict(old.execute("SELECT * FROM sources WHERE source_id='source_aza_jobs_board'").fetchone() or {}) if 'sources' in present else None
    career_names={r['career_id']:r['name'] for r in old.execute('SELECT career_id,name FROM career_roles')} if 'career_roles' in present else {}
    tables={}
    for table in MARKET_TABLES:
        if table not in present: continue
        tables[table]=[dict(r) for r in old.execute(f'SELECT * FROM {table}')]
        if table=='market_job_role_matches':
            for row in tables[table]: row['_career_name']=career_names.get(row['career_id'])
    old.close()
    return {'source':source,'tables':tables}

def restore_rows(con,table,records,career_ids):
    if not records:return
    columns={r[1] for r in con.execute(f'PRAGMA table_info({table})')}
    for original in records:
        row=dict(original)
        career_name=row.pop('_career_name',None)
        if table=='market_job_role_matches':
            if not career_name or career_name not in career_ids: continue
            row['career_id']=career_ids[career_name]
        row={k:v for k,v in row.items() if k in columns}
        names=list(row)
        con.execute(f"INSERT OR REPLACE INTO {table} ({','.join(names)}) VALUES ({','.join('?' for _ in names)})",[row[k] for k in names])

def slug(s:str)->str:
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def family_for(name, category):
    n=name.lower()
    if category.startswith('Animal behavior'):
        if any(k in n for k in ['welfare','husbandry','enrichment']): return 'rf_welfare_husbandry'
        if any(k in n for k in ['trainer','service-dog','behaviorist / applied']): return 'rf_applied_behavior'
        if any(k in n for k in ['shelter','companion']): return 'rf_shelter_companion'
        return 'rf_behavior_research'
    if category.startswith('Zoos'):
        if 'aquarist' in n: return 'rf_aquatic_care'
        if 'conservation-breeding' in n: return 'rf_population'
        if any(k in n for k in ['collection','curator','conservation coordinator','research coordinator']): return 'rf_zoo_science_leadership'
        if any(k in n for k in ['behavioral-husbandry','welfare','behavioral researcher']): return 'rf_welfare_husbandry'
        return 'rf_animal_care'
    if category.startswith('Wildlife'):
        if any(k in n for k in ['rehabilitator','rehabilitation / release coordinator']): return 'rf_rehab'
        if any(k in n for k in ['reintroduction','post-release','endangered-species']): return 'rf_reintroduction'
        if any(k in n for k in ['movement','spatial']): return 'rf_movement'
        if any(k in n for k in ['disease','ecophysiology']): return 'rf_wildlife_health'
        if 'human-wildlife' in n: return 'rf_human_dimensions'
        if 'habitat / wildlife management' in n: return 'rf_habitat'
        if 'technician' in n: return 'rf_wildlife_tech'
        return 'rf_wildlife_biology'
    if category.startswith('Organismal'):
        if any(k in n for k in ['physiologist','neuroethologist']): return 'rf_physiology'
        if 'evolutionary' in n or 'field ecologist' in n or 'ecological research' in n: return 'rf_evolution'
        return 'rf_taxon'
    if category.startswith('Quantitative'):
        if re.search(r'\bgis\b',n) or 'spatial analyst' in n: return 'rf_gis'
        if 'quantitative' in n or 'biometrician' in n: return 'rf_quant'
        if any(k in n for k in ['consultant','permitting','compliance']): return 'rf_env_consult'
        if 'restoration' in n or 'monitoring specialist' in n: return 'rf_restoration'
        return 'rf_agency'
    if category.startswith('Research'):
        if n.startswith('m.s.') or n.startswith('m.s. / ph.d.'): return 'rf_grad'
        if any(k in n for k in ['principal investigator','professor']): return 'rf_independent_research'
        return 'rf_research_support'
    if category.startswith('Education'):
        if 'zoo / aquarium educator' in n: return 'rf_zoo_education'
        if any(k in n for k in ['wildlife / environmental','naturalist','outreach']): return 'rf_wildlife_education'
        return 'rf_scicomm'
    return 'rf_research_support'

def role_kind(c):
    status=(c.get('details',{}).get('Market status','') or '').upper()
    if status.startswith('EDU') or 'Graduate study pathway' in (c.get('educationBand') or ''): return 'education_path'
    if 'later career' in (c.get('educationBand') or '').lower(): return 'later_career'
    if status.startswith('F'): return 'scientific_specialty'
    return 'career'

def evidence_status(c):
    status=(c.get('details',{}).get('Market status','') or '').upper()
    if status.startswith('E'): return 'verified_occupation_or_title'
    if status.startswith('R'): return 'verified_function_title_varies'
    if status.startswith('F'): return 'established_scientific_specialty'
    if status.startswith('EDU'): return 'education_path'
    return 'supported'

def career_stage(c):
    n=c['name'].lower(); e=(c.get('educationBand') or '').lower()
    if 'graduate study pathway' in e: return 'education'
    if 'later career' in e or any(k in n for k in ['curator','manager','principal investigator','professor']): return 'leadership'
    if any(k in n for k in ['technician','assistant','keeper','caretaker','caregiver','trainer','aquarist','educator','naturalist','rehabilitator']): return 'entry_or_early'
    if any(k in n for k in ['coordinator','specialist','scientist','biologist','ecologist','zoologist','mammalogist','ornithologist','herpetologist','physiologist','consultant']): return 'professional_or_specialist'
    return 'variable'

def split_aliases(c):
    out=[]
    for key,atype in [('Searchable job titles','searchable_title'),('Alternate names / terms','alternate_term')]:
        val=(c.get('details') or {}).get(key)
        if val:
            for a in [x.strip() for x in str(val).split(';') if x.strip()]: out.append((a,atype))
    return out

def main():
    market_backup=snapshot_market_data()
    if DB.exists(): DB.unlink()
    con=sqlite3.connect(DB);con.execute('PRAGMA foreign_keys=ON');con.executescript(SCHEMA.read_text())
    con.execute('INSERT INTO ingest_batches VALUES (?,?,?,?,?,?)',('batch_20260908_market_expansion','legacy migration + 2026 market-validation expansion',TODAY,None,'running','Initial normalized research-database build from explicit import files.'))
    con.executemany('INSERT INTO domains VALUES (?,?,?)',seed['domains'])
    con.executemany('INSERT INTO role_families VALUES (?,?,?,?)',seed['role_families'])
    con.executemany('INSERT INTO metadata(key,value) VALUES (?,?)',[
        ('schema_version','1.1'),('dataset_version','2026-09-08.2'),('retrieved_date',TODAY),('canonical_source','SQLite'),
        ('seed_file',SEED.name),('legacy_import',LEGACY.name),('notes','Normalized migration plus 2026 real-market validation expansion; site JSON is a generated publication artifact.')])
    con.executemany('INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?)',seed['sources'])
    if market_backup['source']:
        src=market_backup['source']; cols=list(src)
        con.execute(f"INSERT OR IGNORE INTO sources ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",[src[k] for k in cols])

    program_ids={}
    for p in legacy['programs']:
        pid='prg_'+p['code'].lower().replace('-','_');program_ids[p['code']]=pid
        con.execute('INSERT INTO programs(program_id,code,school,title,program_type,profile_json,last_verified) VALUES (?,?,?,?,?,?,?)',(pid,p['code'],p['school'],p['title'],p.get('type'),json.dumps(p,ensure_ascii=False),TODAY))

    career_ids={};seq=1;aliases=[]
    for c in legacy['careers']:
        cid=f'cr_{seq:04d}';seq+=1;career_ids[c['name']]=cid
        fam=family_for(c['name'],c['category']);desc=c.get('roleFocus') or c.get('details',{}).get('Typical education / progression','')
        con.execute('''INSERT INTO career_roles(career_id,family_id,name,slug,role_kind,market_status,evidence_status,description,education_summary,direct_animal_contact,career_stage,last_verified,source_origin)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(cid,fam,c['name'],slug(c['name']),role_kind(c),c.get('details',{}).get('Market status'),evidence_status(c),desc,c.get('educationBand'),c.get('directContact'),career_stage(c),TODAY,'legacy_researched_matrix'))
        for k,score in zip(DIM_KEYS,c.get('dims',[0]*10)):con.execute('INSERT INTO career_dimensions VALUES (?,?,?)',(cid,k,float(score)))
        for tag in c.get('workTags',[]):con.execute('INSERT INTO career_work_tags VALUES (?,?)',(cid,tag))
        for code,supp in c.get('support',{}).items():con.execute('INSERT INTO career_program_support(career_id,program_id,support_code,source_origin) VALUES (?,?,?,?)',(cid,program_ids[code],supp,'legacy_researched_matrix'))
        aliases += [(cid,a,t,'legacy_researched_matrix') for a,t in split_aliases(c)]
    for c in seed['new_roles']:
        cid=f'cr_{seq:04d}';seq+=1;career_ids[c['name']]=cid
        con.execute('''INSERT INTO career_roles(career_id,family_id,name,slug,role_kind,market_status,evidence_status,description,education_summary,direct_animal_contact,career_stage,last_verified,source_origin)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(cid,c['family_id'],c['name'],slug(c['name']),c['role_kind'],c['market_status'],c['evidence_status'],c['description'],c['educationBand'],c['directContact'],c['career_stage'],TODAY,'2026_market_expansion'))
        for k,score in zip(DIM_KEYS,c['dims']):con.execute('INSERT INTO career_dimensions VALUES (?,?,?)',(cid,k,float(score)))
        for tag in c['workTags']:con.execute('INSERT INTO career_work_tags VALUES (?,?)',(cid,tag))
        for code,supp in c['support'].items():con.execute('INSERT INTO career_program_support(career_id,program_id,support_code,source_origin) VALUES (?,?,?,?)',(cid,program_ids[code],supp,'2026_market_expansion'))
        aliases += [(cid,a,t,'2026_market_expansion') for a,t in split_aliases(c)]
    for table in ['market_job_postings','market_job_classifications','market_job_scrape_runs','market_job_role_matches']:
        restore_rows(con,table,market_backup['tables'].get(table,[]),career_ids)
    for i,(cid,a,t,origin) in enumerate(aliases,1):
        con.execute('INSERT OR IGNORE INTO career_aliases(alias_id,career_id,alias,alias_type,verification_status) VALUES (?,?,?,?,?)',(f'alias_{i:04d}',cid,a,t,'curated_search_term'))

    con.executemany('INSERT INTO competencies VALUES (?,?,?,?)',seed['competencies'])
    for code,vals in seed['program_competencies'].items():
        for comp,strength in vals.items():con.execute('INSERT INTO program_competencies VALUES (?,?,?,?)',(program_ids[code],comp,strength,'Curated from current program curriculum/profile research.'))
    for c in legacy['careers']:
        cid=career_ids[c['name']];blob=(c['name']+' '+c.get('roleFocus','')+' '+' '.join(c.get('workTags',[]))+' '+json.dumps(c.get('details',{}))).lower()
        for comp,keys in seed['keyword_competencies']:
            if any(k in blob for k in keys):con.execute('INSERT OR IGNORE INTO career_competencies VALUES (?,?,?)',(cid,comp,'important'))
    for name,comps in seed['new_role_competencies'].items():
        for comp in comps:con.execute('INSERT OR IGNORE INTO career_competencies VALUES (?,?,?)',(career_ids[name],comp,'important'))

    for i,p in enumerate(seed['job_postings'],1):
        name,title,emp,loc,pdate,ed,exp,smin,smax,sunit,src,url,notes=p;cid=career_ids[name];pid=f'post_{i:04d}'
        con.execute('''INSERT INTO job_postings(posting_id,career_id,title,employer,location,posted_date,retrieved_date,education_min,experience_min,salary_min,salary_max,salary_unit,source_id,url,active_status,notes)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(pid,cid,title,emp,loc,pdate,TODAY,ed,exp,smin,smax,sunit,src,url,'current_or_recent',notes))
        con.execute('INSERT INTO observed_titles VALUES (?,?,?,?,?,?,?,?,?)',(f'obs_post_{i:04d}',cid,title,emp,loc,'job_posting',pdate or TODAY,src,notes))
        if smin is not None:
            amin=smin;amax=smax if smax is not None else smin
            if sunit=='hourly':amin*=2080;amax*=2080
            con.execute('INSERT INTO salary_observations VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(f'sal_{i:04d}',cid,pid,'job_posting',loc,smin,smax,sunit,amin,amax,pdate or TODAY,notes))
    for i,o in enumerate(seed['observed_titles'],1):
        name,title,org,loc,otype,odate,src,notes=o
        con.execute('INSERT INTO observed_titles VALUES (?,?,?,?,?,?,?,?,?)',(f'obs_dir_{i:04d}',career_ids[name],title,org,loc,otype,odate,src,notes))

    con.executemany('INSERT INTO credentials VALUES (?,?,?,?,?,?)',seed['credentials'])
    for name,cred,rel,notes in seed['career_credentials']:con.execute('INSERT INTO career_credentials VALUES (?,?,?,?)',(career_ids[name],cred,rel,notes))
    for qid,name,org,series,qname,edu,course,exp,src in seed['qualification_profiles']:
        con.execute('INSERT INTO qualification_profiles VALUES (?,?,?,?,?,?,?,?,?)',(qid,career_ids[name],org,series,qname,edu,course,exp,src))
    for i,e in enumerate(seed['progression_edges'],1):
        frm,to,rel,typ,edu,exp,status,src,notes=e
        con.execute('INSERT INTO career_edges VALUES (?,?,?,?,?,?,?,?,?,?)',(f'edge_{i:04d}',career_ids[frm],career_ids[to],rel,typ,edu,exp,status,src,notes))
    for i,e in enumerate(seed['evidence_claims'],1):
        cid=career_ids[e['career_name']]
        con.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?)',(f'ev_{i:04d}',e['entity_type'],cid,e['claim_type'],e['claim_value'],e['source_id'],e['confidence'],e['verification_status'],e.get('valid_from'),e['last_verified'],e.get('notes')))

    con.execute("""UPDATE career_roles SET evidence_status='verified_current_market'
                   WHERE career_id IN (
                     SELECT DISTINCT career_id FROM job_postings
                     UNION
                     SELECT DISTINCT m.career_id FROM market_job_role_matches m
                     JOIN market_job_classifications c ON c.posting_id=m.posting_id
                     JOIN market_job_postings p ON p.posting_id=m.posting_id
                     WHERE m.reviewed=1 AND c.reviewed=1 AND c.relevance_status='in_scope'
                       AND p.active_status='active'
                   ) AND role_kind!='education_path'""")
    review_i=0
    for cid,name,kind in con.execute('SELECT career_id,name,role_kind FROM career_roles WHERE active=1'):
        if kind=='education_path':continue
        obs=con.execute('SELECT COUNT(*) FROM observed_titles WHERE career_id=?',(cid,)).fetchone()[0]
        posts=con.execute('SELECT COUNT(*) FROM job_postings WHERE career_id=?',(cid,)).fetchone()[0]
        edges=con.execute('SELECT COUNT(*) FROM career_edges WHERE from_career_id=? OR to_career_id=?',(cid,cid)).fetchone()[0]
        if obs==0:
            review_i+=1;con.execute('INSERT INTO review_queue VALUES (?,?,?,?,?,?,?,?,?)',(f'review_{review_i:04d}','career',cid,'observed_title_coverage','high','open',TODAY,None,'Find authoritative employer/professional examples of actual titles.'))
        elif posts==0:
            review_i+=1;con.execute('INSERT INTO review_queue VALUES (?,?,?,?,?,?,?,?,?)',(f'review_{review_i:04d}','career',cid,'current_posting_coverage','medium','open',TODAY,None,'Add current/recent posting evidence when available.'))
        if edges==0 and kind not in ('scientific_specialty','later_career'):
            review_i+=1;con.execute('INSERT INTO review_queue VALUES (?,?,?,?,?,?,?,?,?)',(f'review_{review_i:04d}','career',cid,'progression_coverage','low','open',TODAY,None,'Research explicit natural-growth, lateral, or specialization transitions.'))
    con.execute('UPDATE ingest_batches SET completed_at=?,status=? WHERE batch_id=?',(TODAY,'complete','batch_20260908_market_expansion'))
    con.commit();con.close();print(f'Built {DB}')

if __name__=='__main__':main()
