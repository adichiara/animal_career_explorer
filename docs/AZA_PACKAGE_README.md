# AZA Job Scraper Package

This portable package adds complete-board AZA Jobs collection, conservative scope classification, canonical-role match proposals, human review, and CSV export to the Animal Career Data Project.

Copy the `database/`, `docs/`, and `scripts/` folders into the project root, preserving their paths. The project must already contain `database/careers.sqlite` with the core career tables.

Run:

```bash
pip install playwright
playwright install chromium
python scripts/scrape_aza_jobs.py
python scripts/propose_aza_job_matches.py
python scripts/review_aza_job_matches.py
```

Review `exports/aza_job_match_review.csv`, fill the decision columns, then run:

```bash
python scripts/review_aza_job_matches.py --import-reviewed
python scripts/export_aza_jobs.py
```

The scraper defaults to a 30-second delay. It stores structured facts and concise derived summaries rather than full job-description text. Rule-generated suggestions never overwrite reviewed decisions, and only reviewed in-scope matches are eligible for website publication.
