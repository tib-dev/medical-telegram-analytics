select
    message_id,
    view_count
from {{ ref('stg_telegram_messages') }}
where view_count < 0
