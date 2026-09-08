# Animal Career Data Project — Validation Report

**Validation date:** 2026-09-08

## Result

- **Errors:** 0
- **Warnings:** 0
- **Foreign-key violations:** 0

## Database scope

- Domains: **7**
- Role families: **32**
- Canonical career roles/pathways: **93**
- Curated search aliases: **538**
- Observed market titles: **71**
- Current/recent job-posting observations: **58**
- Salary observations from postings: **20**
- Competencies: **26**
- Credentials: **7**
- Formal qualification profiles: **5**
- Explicit career-progression edges: **48**
- Registered sources: **44**
- Explicit evidence claims: **19**
- Open research-review items: **81**
- Ingest batches recorded: **1**
- Change-log entries: **0**

## AZA complete-board ingestion

- Market-board postings captured: **0**
- Scope classifications: **0**
- Proposed/reviewed canonical-role links: **0**
- Human-reviewed classifications: **0**
- Accepted reviewed job-to-role links: **0**
- Scrape runs recorded: **0**

Complete-board listings remain separate from curated career evidence. Only reviewed, in-scope role matches are published into career profiles.

## Evidence coverage

- Roles with at least one observed title: **37/93**
- Roles with a current/recent posting in this research snapshot: **31/93**
- Roles with an explicit evidence claim: **18/93**
- Roles connected to at least one explicit progression edge: **52/93**

A role without a current posting is **not** treated as nonexistent. Current postings are observations of the labor market at one point in time; role existence can also be supported by professional organizations, employer staff directories, federal occupational series, and established scientific specialties.

### Career evidence-status distribution

- verified_current_market: **31**
- verified_function_title_varies: **23**
- verified_occupation_or_title: **22**
- established_scientific_specialty: **10**
- verified_professional_role: **6**
- verified_professional_assignment: **1**

### Source authority tiers

- Tier A: **14** sources
- Tier B: **12** sources
- Tier C: **18** sources

### Source types

- job_posting: **23**
- qualification_standard: **5**
- professional_reference: **4**
- job_board: **4**
- credential_standard: **4**
- employee_directory: **3**
- permit_standard: **1**

## Freshness

- Sources retrieved within the last 365 days: **44/44**
- Sources older than 365 days or with unparseable retrieval date: **0**

## Important interpretation rules

- **Canonical role ≠ employer title.** Canonical roles organize the exploration experience; observed titles preserve what employers/professional organizations actually call the work.
- **Job postings are observations, not the definition of a field.** They are used to validate titles, qualifications, duties, salary ranges, and progression patterns.
- **O*NET/BLS data remain broad benchmarks.** Niche animal-care, welfare, zoo, rehabilitation, and conservation roles use posting-level and professional-organization evidence when a dedicated occupation code does not exist.
- **Program support is analytical.** S/C/G/N support mappings summarize curriculum fit and should be periodically revalidated as curricula change.
- **Progression edges are not guaranteed promotions.** They represent observed or professionally plausible transitions; edge-level evidence status distinguishes stronger from more inferential relationships.

## Managed research-review queue

Known evidence gaps are materialized in the database rather than hidden. The current open queue contains:
- observed_title_coverage (high priority): **50**
- progression_coverage (low priority): **25**
- current_posting_coverage (medium priority): **6**

## Review priorities for the next research cycle

1. Expand posting observations for career families with few or no current examples, especially shelter behavior, sanctuary work, cognition research, and conservation-breeding/population roles.
2. Add posting-specific education and experience fields where source pages provide them.
3. Expand salary observations so niche roles rely less on broad occupation proxies.
4. Add more explicit source-backed progression edges from real job ladders and employer classifications.
5. Revalidate all ten undergraduate program competency mappings against 2027–2028 catalogs before application decisions.

Full row-level evidence coverage is exported to `career_evidence_coverage.csv`.
