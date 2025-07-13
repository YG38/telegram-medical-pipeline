"""Detect objects in scraped images with YOLOv8 and insert results into Postgres.
Assumes images are stored alongside JSONL files at data/raw/<date>/<channel>/<msg_id>.jpg
For demo purposes, we treat every image found in data/raw as a candidate.
The script will:
1. Traverse data/raw looking for *.jpg / *.png
2. Run YOLOv8 pre-trained model (coco) via ultralytics.
3. Insert detection rows into postgres table raw.image_detections (created if absent).
   Columns: image_path, message_id, object_class, confidence
"""
from __future__ import annotations

import os
import re
from glob import glob
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()
MODEL = YOLO("yolov8n.pt")  # lightweight model
RAW_DIR = Path("data/raw")
IMG_PATTERNS = ["*.jpg", "*.jpeg", "*.png"]

DSN = "dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}".format(
    **{k: os.environ[k] for k in [
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
    ]}
)

MESSAGE_ID_RE = re.compile(r"(\d+)\.(?:jpg|jpeg|png)$", re.I)


def ensure_table(cur):
    cur.execute(
        """
        CREATE SCHEMA IF NOT EXISTS raw;
        CREATE TABLE IF NOT EXISTS raw.image_detections (
            image_path TEXT,
            message_id BIGINT,
            object_class TEXT,
            confidence NUMERIC,
            PRIMARY KEY (image_path, object_class, confidence)
        );
        """
    )


def process_image(cur, img_path: Path):
    msg_id_match = MESSAGE_ID_RE.search(img_path.name)
    message_id = int(msg_id_match.group(1)) if msg_id_match else None

    results = MODEL(img_path, verbose=False)
    for r in results:
        for c, conf in zip(r.boxes.cls.tolist(), r.boxes.conf.tolist()):
            class_name = MODEL.model.names[int(c)]
            cur.execute(
                """INSERT INTO raw.image_detections (image_path, message_id, object_class, confidence)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;""",
                (str(img_path), message_id, class_name, float(conf)),
            )


def main():
    conn = psycopg2.connect(DSN)
    conn.autocommit = True
    cur = conn.cursor()
    ensure_table(cur)

    img_files = []
    for pattern in IMG_PATTERNS:
        img_files.extend(RAW_DIR.rglob(pattern))

    for img in img_files:
        process_image(cur, img)
        print(f"Processed {img}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
