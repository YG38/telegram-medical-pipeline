"""Load raw JSONL files from data/raw into a PostgreSQL schema called raw.telegram_messages."""
from __future__ import annotations

import json
import os
from glob import glob
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

RAW_PATH = Path("data/raw")
DSN = "dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}".format(
    **{k: os.environ[k] for k in [
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
    ]}
)

def create_table(cur):
    cur.execute(
        """
        CREATE SCHEMA IF NOT EXISTS raw;
        CREATE TABLE IF NOT EXISTS raw.telegram_messages (
            id BIGINT PRIMARY KEY,
            date TIMESTAMP,
            message TEXT,
            sender_id BIGINT,
            chat_id BIGINT,
            has_media BOOLEAN,
            raw_json JSONB
        );
        """
    )


def load_file(cur, file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            cur.execute(
                """INSERT INTO raw.telegram_messages (id, date, message, sender_id, chat_id, has_media, raw_json)
                VALUES (%(id)s, %(date)s, %(message)s, %(sender_id)s, %(chat_id)s, %(has_media)s, %(raw)s)
                ON CONFLICT (id) DO NOTHING;""",
                {
                    "id": record["id"],
                    "date": record["date"],
                    "message": record["message"],
                    "sender_id": record["sender_id"],
                    "chat_id": record["chat_id"],
                    "has_media": record["has_media"],
                    "raw": json.dumps(record),
                },
            )


def main():
    conn = psycopg2.connect(DSN)
    conn.autocommit = True
    cur = conn.cursor()
    create_table(cur)

    for jsonl in glob(str(RAW_PATH / "*/*.jsonl")):
        load_file(cur, Path(jsonl))
        print(f"Loaded {jsonl}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
