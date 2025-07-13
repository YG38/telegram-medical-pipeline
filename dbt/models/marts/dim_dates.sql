with dates as (
    select generate_series(
        (select min(message_ts) from {{ ref('stg_telegram_messages') }}),
        (select max(message_ts) from {{ ref('stg_telegram_messages') }}),
        '1 day'::interval
    ) as day
)
select
    day::date as date_id,
    extract(year from day) as year,
    extract(month from day) as month,
    extract(day from day) as day_of_month,
    extract(dow from day) as day_of_week
from dates;
