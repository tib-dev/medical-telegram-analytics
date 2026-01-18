with channel_data as (

    select
        channel_name,
        min(message_date) as first_post_date,
        max(message_date) as last_post_date,
        count(*) as total_posts,
        avg(view_count) as avg_views
    from {{ ref('stg_telegram_messages') }}
    group by channel_name

)

select
    row_number() over (order by channel_name) as channel_key,
    channel_name,
    'Medical' as channel_type,
    first_post_date,
    last_post_date,
    total_posts,
    avg_views
from channel_data
