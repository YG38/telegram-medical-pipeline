with msgs as (
    select distinct chat_id from {{ ref('stg_telegram_messages') }}
)
select
    chat_id as channel_id,
    'telegram' as platform
from msgs;
