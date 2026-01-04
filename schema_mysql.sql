CREATE DATABASE IF NOT EXISTS messenger_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE messenger_bot;

CREATE TABLE IF NOT EXISTS fb_users (
  psid VARCHAR(64) PRIMARY KEY,
  first_seen_at DATETIME NULL,
  last_seen_at DATETIME NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  note VARCHAR(255) NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS conversations (
  id VARCHAR(64) PRIMARY KEY,
  updated_time DATETIME NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS messages (
  id VARCHAR(64) PRIMARY KEY,
  conversation_id VARCHAR(64) NULL,
  psid VARCHAR(64) NULL,
  direction ENUM('in','out') NOT NULL,
  text TEXT NULL,
  created_time DATETIME NULL,
  raw_json JSON NULL,
  INDEX idx_conv_time (conversation_id, created_time),
  INDEX idx_psid_time (psid, created_time)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS events (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  psid VARCHAR(64) NULL,
  type VARCHAR(50) NOT NULL,
  detail TEXT NULL,
  created_at DATETIME NOT NULL
) ENGINE=InnoDB;