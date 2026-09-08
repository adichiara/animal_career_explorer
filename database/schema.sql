PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS metadata (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS domains (
  domain_id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT
);

CREATE TABLE IF NOT EXISTS role_families (
  family_id TEXT PRIMARY KEY,
  domain_id TEXT NOT NULL REFERENCES domains(domain_id),
  name TEXT NOT NULL,
  description TEXT,
  UNIQUE(domain_id, name)
);

CREATE TABLE IF NOT EXISTS career_roles (
  career_id TEXT PRIMARY KEY,
  family_id TEXT NOT NULL REFERENCES role_families(family_id),
  name TEXT NOT NULL UNIQUE,
  slug TEXT NOT NULL UNIQUE,
  role_kind TEXT NOT NULL DEFAULT 'career',
  market_status TEXT,
  evidence_status TEXT NOT NULL DEFAULT 'supported',
  description TEXT,
  education_summary TEXT,
  direct_animal_contact TEXT,
  career_stage TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  last_verified TEXT,
  source_origin TEXT
);

CREATE TABLE IF NOT EXISTS career_dimensions (
  career_id TEXT NOT NULL REFERENCES career_roles(career_id) ON DELETE CASCADE,
  dim_key TEXT NOT NULL,
  score REAL NOT NULL,
  PRIMARY KEY (career_id, dim_key)
);

CREATE TABLE IF NOT EXISTS career_work_tags (
  career_id TEXT NOT NULL REFERENCES career_roles(career_id) ON DELETE CASCADE,
  tag TEXT NOT NULL,
  PRIMARY KEY (career_id, tag)
);

CREATE TABLE IF NOT EXISTS programs (
  program_id TEXT PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  school TEXT NOT NULL,
  title TEXT NOT NULL,
  program_type TEXT,
  profile_json TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  last_verified TEXT
);

CREATE TABLE IF NOT EXISTS career_program_support (
  career_id TEXT NOT NULL REFERENCES career_roles(career_id) ON DELETE CASCADE,
  program_id TEXT NOT NULL REFERENCES programs(program_id) ON DELETE CASCADE,
  support_code TEXT NOT NULL,
  rationale TEXT,
  source_origin TEXT,
  PRIMARY KEY (career_id, program_id)
);

CREATE TABLE IF NOT EXISTS competencies (
  competency_id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  category TEXT NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS career_competencies (
  career_id TEXT NOT NULL REFERENCES career_roles(career_id) ON DELETE CASCADE,
  competency_id TEXT NOT NULL REFERENCES competencies(competency_id) ON DELETE CASCADE,
  importance TEXT NOT NULL,
  PRIMARY KEY (career_id, competency_id)
);

CREATE TABLE IF NOT EXISTS program_competencies (
  program_id TEXT NOT NULL REFERENCES programs(program_id) ON DELETE CASCADE,
  competency_id TEXT NOT NULL REFERENCES competencies(competency_id) ON DELETE CASCADE,
  strength REAL NOT NULL,
  evidence_note TEXT,
  PRIMARY KEY (program_id, competency_id)
);

CREATE TABLE IF NOT EXISTS sources (
  source_id TEXT PRIMARY KEY,
  organization TEXT NOT NULL,
  source_type TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  published_date TEXT,
  retrieved_date TEXT NOT NULL,
  authority_tier TEXT NOT NULL,
  notes TEXT
);


CREATE TABLE IF NOT EXISTS career_aliases (
  alias_id TEXT PRIMARY KEY,
  career_id TEXT NOT NULL REFERENCES career_roles(career_id) ON DELETE CASCADE,
  alias TEXT NOT NULL,
  alias_type TEXT NOT NULL,
  source_id TEXT REFERENCES sources(source_id),
  verification_status TEXT NOT NULL DEFAULT 'search_term',
  UNIQUE(career_id, alias, alias_type)
);

CREATE TABLE IF NOT EXISTS ingest_batches (
  batch_id TEXT PRIMARY KEY,
  scope TEXT NOT NULL,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  status TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS review_queue (
  review_id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  issue_type TEXT NOT NULL,
  priority TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  created_at TEXT NOT NULL,
  reviewed_at TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS change_log (
  change_id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  field_name TEXT,
  old_value TEXT,
  new_value TEXT,
  changed_at TEXT NOT NULL,
  reason TEXT,
  source_id TEXT REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS observed_titles (
  observed_id TEXT PRIMARY KEY,
  career_id TEXT NOT NULL REFERENCES career_roles(career_id),
  title TEXT NOT NULL,
  organization TEXT,
  location TEXT,
  observation_type TEXT NOT NULL,
  observed_date TEXT,
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS job_postings (
  posting_id TEXT PRIMARY KEY,
  career_id TEXT NOT NULL REFERENCES career_roles(career_id),
  title TEXT NOT NULL,
  employer TEXT NOT NULL,
  location TEXT,
  posted_date TEXT,
  retrieved_date TEXT NOT NULL,
  employment_type TEXT,
  education_min TEXT,
  experience_min TEXT,
  salary_min REAL,
  salary_max REAL,
  salary_unit TEXT,
  currency TEXT DEFAULT 'USD',
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  url TEXT NOT NULL,
  active_status TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS salary_observations (
  salary_id TEXT PRIMARY KEY,
  career_id TEXT NOT NULL REFERENCES career_roles(career_id),
  posting_id TEXT REFERENCES job_postings(posting_id),
  source_type TEXT NOT NULL,
  location TEXT,
  salary_min REAL,
  salary_max REAL,
  salary_unit TEXT,
  annualized_min REAL,
  annualized_max REAL,
  observation_date TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS credentials (
  credential_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  organization TEXT NOT NULL,
  credential_type TEXT NOT NULL,
  description TEXT,
  source_id TEXT REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS career_credentials (
  career_id TEXT NOT NULL REFERENCES career_roles(career_id),
  credential_id TEXT NOT NULL REFERENCES credentials(credential_id),
  relationship TEXT NOT NULL,
  notes TEXT,
  PRIMARY KEY (career_id, credential_id)
);

CREATE TABLE IF NOT EXISTS qualification_profiles (
  qualification_id TEXT PRIMARY KEY,
  career_id TEXT REFERENCES career_roles(career_id),
  organization TEXT NOT NULL,
  series_code TEXT,
  name TEXT NOT NULL,
  education_requirement TEXT,
  coursework_requirement TEXT,
  experience_requirement TEXT,
  source_id TEXT NOT NULL REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS career_edges (
  edge_id TEXT PRIMARY KEY,
  from_career_id TEXT NOT NULL REFERENCES career_roles(career_id),
  to_career_id TEXT NOT NULL REFERENCES career_roles(career_id),
  relationship_type TEXT NOT NULL,
  typicality TEXT NOT NULL,
  education_change TEXT,
  experience_change TEXT,
  evidence_status TEXT NOT NULL,
  source_id TEXT REFERENCES sources(source_id),
  notes TEXT,
  UNIQUE(from_career_id, to_career_id, relationship_type)
);

CREATE TABLE IF NOT EXISTS evidence (
  evidence_id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  claim_type TEXT NOT NULL,
  claim_value TEXT NOT NULL,
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  confidence TEXT NOT NULL,
  verification_status TEXT NOT NULL,
  valid_from TEXT,
  last_verified TEXT NOT NULL,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_career_family ON career_roles(family_id);
CREATE INDEX IF NOT EXISTS idx_observed_career ON observed_titles(career_id);
CREATE INDEX IF NOT EXISTS idx_alias_career ON career_aliases(career_id);
CREATE INDEX IF NOT EXISTS idx_alias_text ON career_aliases(alias);
CREATE INDEX IF NOT EXISTS idx_review_status ON review_queue(status, priority);
CREATE INDEX IF NOT EXISTS idx_posting_career ON job_postings(career_id);
CREATE INDEX IF NOT EXISTS idx_posting_date ON job_postings(posted_date);
CREATE INDEX IF NOT EXISTS idx_evidence_entity ON evidence(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_edges_from ON career_edges(from_career_id);
CREATE INDEX IF NOT EXISTS idx_edges_to ON career_edges(to_career_id);


-- AZA/labor-market snapshot extension. Kept in a separate migration for existing DBs.
PRAGMA foreign_keys = ON;

-- Complete labor-market observations from AZA's public job board live independently
-- from the curated career taxonomy. A posting may later map to zero, one, or
-- several canonical career roles.
CREATE TABLE IF NOT EXISTS market_job_postings (
  posting_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  source_external_id TEXT NOT NULL,
  source_url TEXT NOT NULL,
  source_board TEXT NOT NULL DEFAULT 'AZA Jobs',
  title TEXT NOT NULL,
  employer TEXT NOT NULL,
  location_text TEXT,
  city TEXT,
  state_region TEXT,
  country TEXT DEFAULT 'US',
  posted_date TEXT,
  closing_date TEXT,
  anticipated_start_date TEXT,
  retrieved_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  aza_member INTEGER,
  position_type TEXT,
  employment_status TEXT,
  salary_min REAL,
  salary_max REAL,
  salary_unit TEXT,
  currency TEXT DEFAULT 'USD',
  salary_raw TEXT,
  education_level_min TEXT,
  education_field TEXT,
  education_requirements_json TEXT,
  experience_years_min REAL,
  experience_requirements_json TEXT,
  experience_summary TEXT,
  duties_summary TEXT,
  requirements_summary TEXT,
  duty_tags_json TEXT,
  skill_tags_json TEXT,
  credential_tags_json TEXT,
  schedule_tags_json TEXT,
  detail_status TEXT NOT NULL DEFAULT 'pending',
  active_status TEXT NOT NULL DEFAULT 'active',
  listing_page INTEGER,
  raw_text_sha256 TEXT,
  notes TEXT,
  UNIQUE(source_id, source_external_id)
);

CREATE TABLE IF NOT EXISTS market_job_role_matches (
  posting_id TEXT NOT NULL REFERENCES market_job_postings(posting_id) ON DELETE CASCADE,
  career_id TEXT NOT NULL REFERENCES career_roles(career_id) ON DELETE CASCADE,
  match_type TEXT NOT NULL,              -- primary / secondary / adjacent
  confidence REAL NOT NULL,
  method TEXT NOT NULL,                  -- rule / reviewed / model
  reviewed INTEGER NOT NULL DEFAULT 0,
  review_notes TEXT,
  PRIMARY KEY (posting_id, career_id)
);

CREATE TABLE IF NOT EXISTS market_job_classifications (
  posting_id TEXT PRIMARY KEY REFERENCES market_job_postings(posting_id) ON DELETE CASCADE,
  relevance_status TEXT NOT NULL,
  confidence REAL NOT NULL,
  method TEXT NOT NULL,
  rationale TEXT,
  reviewed INTEGER NOT NULL DEFAULT 0,
  reviewed_at TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS market_job_scrape_runs (
  run_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  started_at TEXT NOT NULL,
  completed_at TEXT,
  status TEXT NOT NULL,
  listings_discovered INTEGER NOT NULL DEFAULT 0,
  details_scraped INTEGER NOT NULL DEFAULT 0,
  details_failed INTEGER NOT NULL DEFAULT 0,
  pages_discovered INTEGER NOT NULL DEFAULT 0,
  crawl_delay_seconds REAL,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_market_jobs_posted ON market_job_postings(posted_date);
CREATE INDEX IF NOT EXISTS idx_market_jobs_employer ON market_job_postings(employer);
CREATE INDEX IF NOT EXISTS idx_market_jobs_title ON market_job_postings(title);
CREATE INDEX IF NOT EXISTS idx_market_jobs_active ON market_job_postings(active_status, posted_date);
CREATE INDEX IF NOT EXISTS idx_market_job_matches_career ON market_job_role_matches(career_id, confidence);
CREATE INDEX IF NOT EXISTS idx_market_job_classification_status ON market_job_classifications(relevance_status, reviewed);
