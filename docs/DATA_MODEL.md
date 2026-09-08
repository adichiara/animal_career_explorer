# Data Model

## Core taxonomy

### `domains`
The broadest navigational level, such as animal behavior/welfare, managed animals, wildlife/conservation, or quantitative/environmental science.

### `role_families`
A middle layer used to prevent the explorer from becoming a flat list of hundreds of titles. Examples include Welfare, Enrichment & Behavioral Husbandry; Species Recovery & Reintroduction; or Quantitative Ecology & Data Science.

### `career_roles`
Stable canonical concepts presented to users. These are not necessarily literal payroll titles.

Important fields:
- `role_kind`: career, scientific specialty, later-career role, professional assignment, education pathway
- `evidence_status`: distinguishes current-market evidence, verified occupations/functions, professional roles, and established scientific specialties
- `last_verified`: date of most recent curation review

### `career_aliases`
Useful search names and alternate terms. An alias is **not** claimed to have been directly observed in the labor market.

### `observed_titles`
Titles directly observed in job postings, staff directories, or authoritative professional material. This table is intentionally stricter than `career_aliases`.

## Market observations

### `job_postings`
Structured observations of current or recent jobs. The database stores extracted facts rather than relying on the posting text as a permanent career definition.

### `market_job_postings`
Complete-board observations from AZA Jobs. This table intentionally includes both in-scope animal/science work and institutional roles outside the current explorer scope. It stores normalized facts and derived tags/summaries, not full verbatim descriptions.

### `market_job_classifications`
Board-wide scope decisions: `in_scope`, `adjacent`, `out_of_scope`, or `needs_review`. Rule-generated classifications remain visibly unreviewed and are never treated as published career evidence.

### `market_job_role_matches`
Proposed or reviewed links from complete-board postings to canonical roles. A posting may have one primary match and optional secondary matches. Only human-reviewed, in-scope links are published to career profiles.

### `market_job_scrape_runs`
Run-level provenance and completeness counts for resumable AZA board collection.

### `salary_observations`
Posting-level salary evidence. Annualized salary is stored separately from the original unit so hourly and annual postings can be compared without discarding source detail.

### `sources`
Registry of source provenance. Current authority tiers:
- **A:** official government, qualification, permit, or agency sources
- **B:** professional organizations and credentialing bodies
- **C:** individual employer/job-posting observations

### `evidence`
Specific source-backed claims such as a federal coursework rule, permit requirement, or verification that a niche role exists in current professional practice.

## Preparation and progression

### `competencies`
Shared vocabulary connecting careers to college preparation. Examples include behavioral observation, welfare assessment, telemetry, GIS, population biology, statistics, scientific writing and animal husbandry.

### `career_competencies`
Competencies important to a career.

### `program_competencies`
Strength of preparation in each competency for the ten undergraduate paths.

### `career_program_support`
The existing S/C/G/N analytical summary is retained as a high-level comparison, but competency links provide the more explainable layer underneath it.

### `career_edges`
Explicitly curated progression relationships:
- natural growth
- specialization
- management
- research progression
- graduate transition
- lateral movement
- professional assignment

Edges include typicality, expected education/experience change, evidence status and source where available.

### `credentials`, `career_credentials`, `qualification_profiles`
Keeps professional certification, permits and formal qualification standards separate from general education prose.

## Governance tables

### `ingest_batches`
Records major data-ingestion/build cycles.

### `review_queue`
Stores known evidence gaps. The current build automatically creates items for missing observed-title evidence, missing current-posting evidence, and missing explicit progression research.

### `change_log`
Reserved for material changes in future dataset versions so a title mapping, qualification requirement, or program relationship can be traced over time.
