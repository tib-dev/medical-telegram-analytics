
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    full_date as unique_field,
    count(*) as n_records

from telegram_dw."raw_marts"."dim_dates"
where full_date is not null
group by full_date
having count(*) > 1



  
  
      
    ) dbt_internal_test