# Animal Career Data Project

This project is the data-management and publishing layer behind the Animal Pathways reference site.

**Live site:** https://adichiara.github.io/animal_career_explorer/

The project is deliberately designed so the website is **not** the source of truth. Research is stored in a normalized SQLite database, validated, and then published to the browser as generated JSON.

## Current research snapshot

As of 2026-09-08 the database contains:

- 7 broad domains
- 32 role families
- 93 canonical career roles / graduate pathways
- 538 curated search aliases
- 71 directly observed real-world titles
- 58 current/recent job-posting observations
- 20 posting-level salary observations
- 26 competencies
- 7 credentials / permits
- 5 formal qualification profiles
- 48 explicit career-progression relationships
- 44 registered sources, including the AZA complete-board source
- a managed review queue for known evidence gaps

These counts are descriptive of the current research snapshot, not a claim that the career universe is complete.

## Design principles

1. **Canonical role is not the same thing as employer title.** A stable role such as `Wildlife Biologist` can map to many observed employer titles.
2. **Observed titles require evidence.** Search aliases are stored separately from titles actually seen in job postings, staff directories, or professional sources.
3. **Job postings are observations, not definitions.** They support claims about current titles, duties, qualifications, experience and pay, but a role does not cease to exist when no posting is open.
4. **Broad occupation benchmarks stay separate from niche-market evidence.** O*NET/BLS proxies are retained where useful, while job-posting salary observations are stored independently.
5. **Known gaps are explicit.** Missing title, posting or progression evidence becomes a review-queue item rather than being silently hidden.
6. **The website consumes generated data.** `site/data.js` is rebuilt from SQLite; it should not be hand-edited.

## Published site structure

The public homepage links to three article-style reference sections:

- **Field Guides** — 15 long-form guides loaded from editable JSON files in `site/content/areas/`.
- **College Programs** — 17 researched undergraduate pathway guides: the 10-path focused comparison from the validated site export plus 7 additional programs retained from the broader research.
- **Job Examples** — dated, source-backed postings grouped under 37 broader roles. These records illustrate employer titles and requirements; they are not a live job board.

The earlier research interface remains available in `site/legacy.html`, and the earlier preference explorer remains in `site/discover.html`. Both are retained for backward reference but are intentionally absent from the homepage and primary navigation.

## Editing Field Guide content

The explanatory content for `areas.html` is intentionally separate from the generated career database. Each field has a human-editable file under `site/content/areas/`, such as `wildlife-rehabilitation.json`. Editing and committing one of those files updates the live page after GitHub Pages redeploys; `areas.js` does not need to be changed.

See [`site/content/areas/README.md`](site/content/areas/README.md) for the field definitions, examples, JSON rules, and step-by-step editing instructions. The original focused College Program records and all Job Example records come from the validated `site/data.js` export. Seven broader College Program records are editable in [`site/content/programs/additional-programs.json`](site/content/programs/additional-programs.json); editing instructions are in [`site/content/programs/README.md`](site/content/programs/README.md).

## Directory structure

```
Animal_Career_Data_Project/
├── database/
│   ├── careers.sqlite          # canonical source of truth
│   └── schema.sql
├── imports/
│   ├── legacy_site_data.json   # frozen migration input from the earlier prototype
│   └── research_seed_2026-09-08.json # reviewed market/taxonomy research seed
├── scripts/
│   ├── build_database.py
│   ├── validate_database.py
│   ├── export_site_data.py
│   └── patch_site_evidence.py
├── exports/
│   ├── published_data.json
│   ├── careers.csv
│   ├── career_aliases.csv
│   ├── job_postings.csv
│   ├── career_progression_edges.csv
│   ├── sources.csv
│   ├── research_review_queue.csv
│   └── career_evidence_coverage.csv
├── reports/
│   └── validation_report.md
├── docs/
│   └── companion research documents
└── site/
    ├── index.html              # focused three-section homepage
    ├── areas.html              # Field Guides index
    ├── programs.html           # College Programs index
    ├── program.html            # program article renderer
    ├── jobs.html               # Job Examples index
    ├── job.html                # job-example article renderer
    ├── legacy.html             # retained full research interface
    ├── discover.html           # retained preference explorer
    ├── data.js                 # GENERATED from SQLite
    └── content/areas/          # editable Area Explorer content
```

## Rebuild sequence

From the project root:

```bash
python scripts/build_database.py
python scripts/propose_aza_job_matches.py
python scripts/review_aza_job_matches.py
python scripts/validate_database.py
python scripts/export_site_data.py
python scripts/build_artifacts.py
```

`validate_database.py` exits with an error if structural validation fails. The site should be published only after validation succeeds. `build_artifacts.py` creates the standalone HTML, site ZIP, and full project ZIP in `exports/`.

## Research update workflow

New research should follow this sequence:

1. **Collect** — save a source and extract only facts needed for the project.
2. **Normalize** — decide whether a title is a new canonical role, an observed title for an existing role, a search alias, or a specialization.
3. **Review** — confirm source authority, date, role mapping, salary units, qualification claims and progression claims.
4. **Curate** — add the reviewed record to the import seed / database update process.
5. **Validate** — run structural and coverage validation.
6. **Publish** — regenerate site data.
7. **Audit** — record material changes in `change_log` when maintaining future versions.

See `docs/DATA_MODEL.md` and `docs/RESEARCH_WORKFLOW.md` for detail.


## AZA Jobs complete-market ingestion

The project now includes a resumable Playwright scraper for the public AZA Jobs board. It enumerates the board's client-side pagination, follows every `?job=` detail page, and writes normalized facts into `market_job_postings` without forcing unrelated institutional jobs into the animal-career taxonomy. See `docs/AZA_JOB_INGESTION.md`.

> **Current limitation (2026-09-09):** GitHub-hosted Actions runners can enumerate the board but receive a persistent Cloudflare interstitial on detail pages. Do not start a full-board Actions scrape until [issue #1](https://github.com/adichiara/animal_career_explorer/issues/1) is resolved. The scraper now detects and reports this condition without publishing failed detail records.

The scraper defaults to a 30-second request delay in accordance with AZA's published generic crawl-delay and stores structured facts/derived summaries rather than full verbatim job descriptions. A separate conservative rules stage classifies the complete board and proposes canonical-role matches; those suggestions must be reviewed before they appear as career evidence in the website.

Run in a network-enabled environment:

```bash
pip install playwright
playwright install chromium
python scripts/scrape_aza_jobs.py
python scripts/propose_aza_job_matches.py
python scripts/review_aza_job_matches.py
# Review exports/aza_job_match_review.csv, then:
python scripts/review_aza_job_matches.py --import-reviewed
python scripts/export_aza_jobs.py
python scripts/validate_database.py
python scripts/export_site_data.py
python scripts/build_artifacts.py
```

## GitHub Actions

The repository includes `.github/workflows/aza-scrape.yml`. Changes to the scraper or workflow trigger a two-listing smoke test. A manual run can be started from **Actions → AZA jobs scrape and build → Run workflow**, where a test limit can be supplied; `0` requests the complete board.

The workflow installs Chromium, runs the scrape and conservative role-matching stage, validates and rebuilds the project, then uploads a 30-day artifact containing the updated database, review CSV, market export, reports, website package, and master project package. Scrape failures make the workflow fail visibly, while the later diagnostic and artifact-upload steps still run.

Because AZA currently challenges GitHub-hosted runners, `0` should not be used until a permitted working environment or authorized feed is documented and passes a two-listing test. See [issue #1](https://github.com/adichiara/animal_career_explorer/issues/1).
