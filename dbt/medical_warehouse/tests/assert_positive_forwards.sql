select
    message_id,
    forward_count
from {{ ref('stg_telegram_messages') }}
where forward_count < 0
