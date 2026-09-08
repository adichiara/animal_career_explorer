from __future__ import annotations
import sqlite3, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'database'/'careers.sqlite'
p=argparse.ArgumentParser(description='Inspect the managed research-review queue.')
p.add_argument('--priority',choices=['high','medium','low']);p.add_argument('--issue');p.add_argument('--limit',type=int,default=50)
a=p.parse_args();con=sqlite3.connect(DB);con.row_factory=sqlite3.Row
sql='''SELECT q.review_id,q.priority,q.issue_type,q.status,c.name,q.notes FROM review_queue q LEFT JOIN career_roles c ON q.entity_type='career' AND q.entity_id=c.career_id WHERE q.status='open' ''';args=[]
if a.priority:sql+=' AND q.priority=?';args.append(a.priority)
if a.issue:sql+=' AND q.issue_type=?';args.append(a.issue)
sql+=' ORDER BY CASE q.priority WHEN "high" THEN 1 WHEN "medium" THEN 2 ELSE 3 END,c.name LIMIT ?';args.append(a.limit)
for r in con.execute(sql,args):print(f"{r['review_id']}\t{r['priority'].upper()}\t{r['issue_type']}\t{r['name']}\n  {r['notes']}")
