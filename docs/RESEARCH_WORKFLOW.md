# Research and Maintenance Workflow

## 1. Scope control

The project remains focused on the existing interest envelope:

- animal behavior, cognition, learning and communication
- animal welfare, enrichment, behavioral husbandry and training
- zoos, aquariums, sanctuaries and managed wildlife
- wildlife rehabilitation, release and reintroduction
- wildlife biology, ecology, conservation and habitat work
- organismal biology, physiology and neuroethology
- quantitative/spatial/ecological science connected to animal and conservation work
- research, education and communication related to those fields

The goal of expansion is **greater depth and breadth inside this envelope**, not indiscriminate collection of every animal-adjacent occupation.

## 2. Source priorities

### Tier A — primary official sources
Use first for formal requirements and agency/federal roles:
- OPM qualification standards
- USAJOBS / agency career pages
- USFWS permits and programs
- USGS staff/research directories
- official state agency classifications
- official university catalogs for college-path preparation

### Tier B — professional organizations
Use for profession structure, credentials, role definitions, and sector-specific job markets:
- Association of Zoos & Aquariums (AZA)
- The Wildlife Society (TWS)
- National Wildlife Rehabilitators Association (NWRA)
- Animal Behavior Society (ABS)
- recognized behavior/training credentialing organizations

### Tier C — employer observations
Use to validate current titles, job ladders, duties, experience and salary:
- zoo/aquarium employers
- conservation NGOs
- wildlife rehabilitation organizations
- universities/research centers
- consulting/environmental employers

## 3. Classify each new item correctly

Before adding a new "career," ask:

1. Is this genuinely a different kind of work? → possible new canonical role.
2. Is it the same work under another employer title? → `observed_titles` / `career_aliases`.
3. Is it a taxon or employer specialization? → specialization/observed title, not necessarily a new canonical role.
4. Is it a higher responsibility level? → progression edge and observed title.
5. Is it an added professional assignment (e.g., SSP leadership)? → `role_kind=professional_assignment`.
6. Is it a research field whose payroll titles vary? → `role_kind=scientific_specialty`.

This is the main protection against uncontrolled title proliferation.

## 4. Posting extraction fields

For each useful job posting, capture when available:
- actual title
- employer
- location
- posting/retrieval date
- employment type
- minimum education
- minimum experience
- salary min/max and unit
- source URL
- short note explaining why it matters

Do not treat one posting as a universal requirement.

## 5. Progression research

A progression edge should identify:
- source role
- destination role
- relationship type
- whether the transition is common or merely possible
- additional education normally needed
- experience normally needed
- evidence status
- source or rationale

Observed employer ladders and repeated market patterns are stronger evidence than similarity alone. The website may still show similarity-based nearby options, but they are labeled as inferred.

## 6. Refresh cadence

Suggested cadence:
- job-posting samples: quarterly
- salary observations: quarterly when postings are refreshed
- O*NET/BLS benchmarks: annually
- federal qualification standards / permits: annually and when announced changes occur
- professional credentials: annually
- college curricula and support mapping: annually; full refresh before the 2027–2028 application cycle
- taxonomy/progression: as new evidence justifies changes

## 7. Publication gate

A dataset release is publishable only when:
- `PRAGMA foreign_key_check` returns no errors
- each active career has all 10 exploration dimensions
- each active career has support rows for all 10 program paths
- every posting has a registered source and URL
- the validation report has zero structural errors

Coverage gaps are allowed; they must remain visible in `review_queue` and in the site’s Market & Evidence page.
