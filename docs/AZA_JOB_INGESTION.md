# AZA Jobs ingestion

## Purpose

The AZA Jobs board is a particularly valuable market source because its public listing table links to standardized detail pages containing employer-authored descriptions, experience requirements, salary information, and application information. The ingestion process is designed to collect **every listing in the live board snapshot**, not merely jobs already represented in the career taxonomy.

## Why a separate market table

The AZA board includes animal-care and conservation jobs but also finance, development, horticulture, food service, facilities, marketing, IT, veterinary, and other institutional roles. Those should not be forced into the project's animal-career taxonomy. Therefore:

- `market_job_postings` stores the complete observed labor-market snapshot.
- `market_job_role_matches` links only relevant postings to one or more canonical career roles.
- Existing `job_postings` remains the curated subset used directly by career profiles.

## Fields captured

Each listing can contribute:

- AZA job ID and source URL
- title and employer
- location
- AZA member-organization flag
- posted date
- closing date / anticipated start date when present
- full-time / part-time / temporary / seasonal / internship classification
- exempt/non-exempt status when stated
- salary minimum, maximum, and unit when stated
- minimum education level and field when extractable
- minimum years of experience when extractable
- standardized duty tags
- standardized skill tags
- credentials/certifications such as driver's license, SCUBA, veterinary-technician credential, CPR/first aid
- schedule realities such as weekends, holidays, evenings, rotating shifts, overnight work, and travel
- concise derived duty and requirements summaries
- SHA-256 hash of the source page text for change detection
- retrieval date, last-seen date, active status, and scrape status

The database deliberately does **not** store the entire verbatim job description. It stores factual structured fields and concise derived summaries plus the source URL.

## Crawl behavior

The script uses a real browser because the AZA board's pagination is client-side. It:

1. Opens the live job board.
2. Collects all `?job=` links on the current page.
3. Clicks the pagination controls and repeats until no new page is found.
4. Inserts listing stubs immediately, so the run is resumable.
5. Visits each detail page and extracts normalized fields.
6. Upserts changed listings instead of duplicating them.
7. Marks postings not seen in a later **complete** snapshot inactive.

The default `--delay 30` honors the generic 30-second crawl delay published in AZA's robots.txt. A full board scrape may therefore take substantial time; the script is intentionally resumable.

## Current execution limitation

**Status as of 2026-09-09:** GitHub-hosted Actions runners can render and enumerate the AZA Jobs listing table, but individual detail-page requests receive a persistent Cloudflare `Just a moment...` interstitial. GitHub Actions is therefore not currently a supported environment for a complete detail scrape.

Evidence:

- [Initial full-board run](https://github.com/adichiara/animal_career_explorer/actions/runs/34284874727): 280 listings were discovered. The first 149 detail requests timed out and GitHub cancelled the job at its five-hour limit; 131 listings were not attempted.
- [Final two-listing smoke test](https://github.com/adichiara/animal_career_explorer/actions/runs/34343973964): 2 listings were discovered, 0 details were scraped, and both failures explicitly identified a persistent Cloudflare interstitial.
- The initial `-> ok` console messages were incorrect. The former logging expression indicated that an attempt had finished, not that extraction had succeeded. Database counters and saved row statuses showed 0 successful detail pages.

Repairs completed after the initial run:

- Detail navigation no longer waits for `networkidle`, which is unreliable on pages with long-lived background connections.
- A detail page is accepted only when expected job content is present and the response is not an interstitial.
- Persistent Cloudflare pages are reported explicitly.
- Per-listing output now reports the actual success or exception.
- Any detail failure makes the scrape command exit nonzero.
- Workflow push events use a two-listing smoke-test limit; full-board runs require a manual request.
- Diagnostic exports, validation, and artifact upload still run after a scrape failure.

The structural validation report can still show zero database errors after a failed scrape. That means the resulting database is internally consistent; it does **not** mean the detail pages were captured. Confirm `details_scraped`, `details_failed`, and the posting-level `detail_status` values before using an artifact.

Until [issue #1](https://github.com/adichiara/animal_career_explorer/issues/1) is resolved:

1. Do not request a full-board GitHub Actions run.
2. Test any proposed environment with exactly two listings first.
3. Verify extracted fields against the source pages before scaling up.
4. Do not add challenge-bypass, CAPTCHA-solving, or similar behavior. Prefer an interactive local browser/network accepted by AZA or an authorized feed, export, or API.

## Run

```bash
pip install playwright
playwright install chromium
python scripts/scrape_aza_jobs.py --db database/careers.sqlite
python scripts/export_aza_jobs.py
```

Testing only:

```bash
python scripts/scrape_aza_jobs.py --limit 2 --headful
```

## Quality review

Automated extraction should be treated as a first pass. Recommended checks after each complete run:

- detail page failures
- postings with salary text but no parsed salary
- postings with an `Experience Required` section but no extracted education/experience
- unusually high or low salary values
- duplicate titles from the same employer
- unclear location strings
- postings relevant to the career project that remain unmapped to a canonical role

## Classification and role matching

After a scrape, run:

```bash
python scripts/propose_aza_job_matches.py
python scripts/review_aza_job_matches.py
```

The first command gives every board listing one of four scope classifications:

- `in_scope` — a conservative rule found one or more plausible canonical roles
- `adjacent` — animal-sector work outside the current career-map scope
- `out_of_scope` — clearly institutional/support work outside the scope
- `needs_review` — not enough evidence for a safe automatic decision

It also proposes primary/secondary entries in `market_job_role_matches`. The rules favor precision over recall and do not overwrite human-reviewed decisions.

The second command writes `exports/aza_job_match_review.csv`. Reviewers complete:

- `review_decision`: `accept`, `in_scope`, `adjacent`, `out_of_scope`, or `needs_review`
- `reviewed_primary_career_id`: use the suggestion or replace it
- `reviewed_secondary_career_ids`: optional semicolon-separated IDs
- `reviewer_notes`: short rationale for changes or ambiguous cases

Import completed rows with:

```bash
python scripts/review_aza_job_matches.py --import-reviewed
```

Only human-reviewed `in_scope` matches are published into career profiles and posting-level salary summaries. Complete-board records remain available for labor-market analysis without expanding the career taxonomy indiscriminately.

## Publish the reviewed snapshot

```bash
python scripts/export_aza_jobs.py
python scripts/validate_database.py
python scripts/export_site_data.py
python scripts/build_market_audit.py
python scripts/build_artifacts.py
```

`exports/aza_market_jobs.csv` contains the board snapshot, scope classification, review state, and any canonical-role matches. `exports/aza_job_match_review.csv` remains the working review sheet.
