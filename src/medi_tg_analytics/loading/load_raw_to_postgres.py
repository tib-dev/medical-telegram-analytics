import os
import json
import logging
from pathlib import Path
from typing import List, Tuple

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

from medi_tg_analytics.core.settings import settings

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------

load_dotenv()

RAW_DIR: Path = settings.paths.DATA["raw_dir"] / "telegram_messages"
FLAG_FILE: Path = settings.paths.DATA["interim_dir"] / "raw_loaded.flag"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# ------------------------------------------------------------------
# Database connection
# ------------------------------------------------------------------


def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
    except psycopg2.Error as e:
        raise RuntimeError(f"Failed to connect to PostgreSQL: {e}")


# ------------------------------------------------------------------
# Schema & table setup
# ------------------------------------------------------------------

CREATE_SCHEMA_SQL = "CREATE SCHEMA IF NOT EXISTS raw;"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id     BIGINT PRIMARY KEY,
    channel_name   TEXT NOT NULL,
    message_date   TIMESTAMP,
    message_text   TEXT,
    view_count     INT,
    forward_count  INT,
    has_media      BOOLEAN,
    image_path     TEXT,
    ingested_at    TIMESTAMP DEFAULT now()
);
"""

INSERT_SQL = """
INSERT INTO raw.telegram_messages (
    message_id,
    channel_name,
    message_date,
    message_text,
    view_count,
    forward_count,
    has_media,
    image_path
)
VALUES %s
ON CONFLICT (message_id) DO NOTHING;
"""


# ------------------------------------------------------------------
# Loader logic
# ------------------------------------------------------------------

def validate_raw_dir():
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Raw data directory not found: {RAW_DIR}")


def parse_messages(json_path: Path) -> List[Tuple]:
    with open(json_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    rows = []
    for m in messages:
        rows.append(
            (
                m.get("message_id"),
                m.get("channel_name"),
                m.get("message_date"),
                m.get("message_text"),
                m.get("views", 0),
                m.get("forwards", 0),
                m.get("has_media", False),
                m.get("image_path"),
            )
        )

    return rows


def load_json_to_raw():
    validate_raw_dir()

    conn = get_connection()
    cur = conn.cursor()

    # Ensure schema and table exist
    cur.execute(CREATE_SCHEMA_SQL)
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()

    total_inserted = 0
    total_files = 0

    for date_dir in sorted(RAW_DIR.iterdir()):
        if not date_dir.is_dir():
            continue

        for json_file in sorted(date_dir.glob("*.json")):
            rows = parse_messages(json_file)

            if not rows:
                logging.warning(f"No records in {json_file}")
                continue

            execute_values(cur, INSERT_SQL, rows)
            conn.commit()

            total_inserted += len(rows)
            total_files += 1

            logging.info(
                f"Loaded {len(rows)} messages from {json_file.relative_to(RAW_DIR)}"
            )

    cur.close()
    conn.close()

    # DVC marker file
    FLAG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FLAG_FILE, "w") as f:
        f.write("raw telegram messages loaded")

    logging.info(
        f"Completed loading: {total_inserted} messages from {total_files} files"
    )
    logging.info(f"DVC flag written to {FLAG_FILE}")


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    load_json_to_raw()
    print("✅ Raw Telegram data successfully loaded into PostgreSQL")
