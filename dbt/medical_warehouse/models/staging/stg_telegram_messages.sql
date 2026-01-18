with source as (
    select *
    from raw.telegram_messages
)

select
    message_id,
    lower(trim(channel_name)) as channel_name,
    message_date::timestamp as message_date,
    case
        when trim(coalesce(message_text, '')) = '' then null
        else trim(message_text)
    end as message_text,
    coalesce(view_count, 0)::int as view_count,
    coalesce(forward_count, 0)::int as forward_count,
    coalesce(has_media, false)::boolean as has_media,
    image_path,
    length(trim(coalesce(message_text, ''))) as message_length,
    case
        when coalesce(has_media, false) then true
        else false
    end as has_image
from source
where
    -- Only include messages with non-empty text OR with media
    (trim(coalesce(message_text, '')) <> '')
    or coalesce(has_media, false) = true
