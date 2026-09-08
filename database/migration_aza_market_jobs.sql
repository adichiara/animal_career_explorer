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

-- Board-wide scope classification is separate from role matches.  This lets the
-- project account for every AZA listing (including finance, facilities, food
-- service, veterinary work, and other roles outside the current exploration
-- scope) without forcing an inappropriate canonical-role match.
CREATE TABLE IF NOT EXISTS market_job_classifications (
  posting_id TEXT PRIMARY KEY REFERENCES market_job_postings(posting_id) ON DELETE CASCADE,
  relevance_status TEXT NOT NULL,        -- in_scope / adjacent / out_of_scope / needs_review
  confidence REAL NOT NULL,
  method TEXT NOT NULL,                  -- rule / reviewed / model
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
