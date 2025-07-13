from pydantic import BaseModel
from typing import List


class ProductMention(BaseModel):
    product: str
    count: int


class ChannelActivity(BaseModel):
    date: str
    message_count: int


class MessageResult(BaseModel):
    message_id: int
    channel_id: int
    message: str
