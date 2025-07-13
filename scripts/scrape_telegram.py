"""Simple Telegram scraping script that downloads messages from a set of channels
and stores them as JSON lines in data/raw/<YYYY-MM-DD>/<channel>.jsonl

Usage (inside docker container or with env vars loaded):
    python scripts/scrape_telegram.py
"""
from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.custom.message import Message

load_dotenv()

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
SESSION = "telegram_medical"

# Public channels to scrape
DEFAULT_CHANNELS: List[str] = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
]

RAW_DIR = Path("data/raw")


def serialize(msg: Message) -> dict:
    """Convert Telethon Message to dict serializable to JSON."""
    return {
        "id": msg.id,
        "date": msg.date.isoformat() if msg.date else None,
        "message": msg.message,
        "sender_id": getattr(msg.sender_id, "__str__", lambda: None)(),
        "chat_id": getattr(msg.chat_id, "__str__", lambda: None)(),
        "has_media": msg.media is not None,
        "media": None,  # media will be downloaded separately if needed
    }


async def fetch_channel(client: TelegramClient, channel: str, limit: int = 1000):
    print(f"Scraping {channel}…")
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = RAW_DIR / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    outfile = out_dir / f"{channel.split('/')[-1]}.jsonl"

    async for msg in client.iter_messages(entity=channel, limit=limit):
        data = serialize(msg)
        with outfile.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")


async def main(channels: List[str]):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        for chan in channels:
            try:
                await fetch_channel(client, chan)
            except FloodWaitError as e:
                print(f"Hit rate limit: sleeping {e.seconds}s")
                await asyncio.sleep(e.seconds)


if __name__ == "__main__":
    asyncio.run(main(DEFAULT_CHANNELS))
