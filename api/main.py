from fastapi import FastAPI, HTTPException
from typing import List

from .schemas import ProductMention, ChannelActivity, MessageResult
from . import crud

app = FastAPI(title="Telegram Medical Analytics API")


@app.get("/api/reports/top-products", response_model=List[ProductMention])
def top_products(limit: int = 10):
    return crud.get_top_products(limit)


@app.get("/api/channels/{channel_id}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_id: int):
    return crud.get_channel_activity(channel_id)


@app.get("/api/search/messages", response_model=List[MessageResult])
def search_messages(query: str):
    if len(query) < 3:
        raise HTTPException(status_code=400, detail="Query too short")
    return crud.search_messages(query)
