
    
    

select
    full_date as unique_field,
    count(*) as n_records

from telegram_dw."raw_marts"."dim_dates"
where full_date is not null
group by full_date
having count(*) > 1


