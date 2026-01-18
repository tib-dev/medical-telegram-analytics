select
    message_id,
    forward_count
from telegram_dw."raw"."stg_telegram_messages"
where forward_count < 0