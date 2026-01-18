select
    message_id,
    view_count
from telegram_dw."raw"."stg_telegram_messages"
where view_count < 0