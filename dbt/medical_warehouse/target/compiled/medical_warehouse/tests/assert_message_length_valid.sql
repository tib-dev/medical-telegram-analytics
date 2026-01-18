select
    message_id,
    message_text,
    length(trim(message_text)) as message_length
from telegram_dw."raw"."stg_telegram_messages"
where message_text is not null
  and length(trim(message_text)) = 0