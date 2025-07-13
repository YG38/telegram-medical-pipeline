with src as (
    select * from raw.image_detections
)
select
    image_path,
    message_id,
    object_class,
    confidence
from src;
