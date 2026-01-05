CREATE TABLE IF NOT EXISTS fb_users (
  psid VARCHAR(64) PRIMARY KEY,
  first_seen_at TIMESTAMP,
  last_seen_at TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  note VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS conversations (
  id VARCHAR(64) PRIMARY KEY,
  updated_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
  id VARCHAR(64) PRIMARY KEY,
  conversation_id VARCHAR(64),
  psid VARCHAR(64),
  direction VARCHAR(3) CHECK (direction IN ('in','out')),
  text TEXT,
  created_time TIMESTAMP,
  raw_json JSONB
);

CREATE INDEX IF NOT EXISTS idx_conv_time
  ON messages (conversation_id, created_time);

CREATE INDEX IF NOT EXISTS idx_psid_time
  ON messages (psid, created_time);

CREATE TABLE IF NOT EXISTS events (
  id BIGSERIAL PRIMARY KEY,
  psid VARCHAR(64),
  type VARCHAR(50),
  detail TEXT,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bot_settings (
  key VARCHAR(50) PRIMARY KEY,
  value VARCHAR(50) NOT NULL
);

INSERT INTO bot_settings (key, value)
VALUES ('antispam', 'on')
ON CONFLICT (key) DO NOTHING;

INSERT INTO bot_settings (key, value)
VALUES 
  ('antilink', 'on'),
  ('antiqr', 'on')
ON CONFLICT (key) DO NOTHING;