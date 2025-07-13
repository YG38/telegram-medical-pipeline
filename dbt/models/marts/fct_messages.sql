select
    m.message_id,
    d.date_id,
    c.channel_id,
    m.sender_id,
    len(m.message) as message_length,
    m.has_media
from {{ ref('stg_telegram_messages') }} m
left join {{ ref('dim_channels') }} c on m.chat_id = c.channel_id
left join {{ ref('dim_dates') }} d on m.message_ts::date = d.date_id;
