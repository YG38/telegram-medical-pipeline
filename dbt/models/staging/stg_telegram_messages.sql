with src as (
    select * from raw.telegram_messages
)
select
    id as message_id,
    date::timestamp as message_ts,
    chat_id,
    sender_id,
    message,
    has_media
from src;
