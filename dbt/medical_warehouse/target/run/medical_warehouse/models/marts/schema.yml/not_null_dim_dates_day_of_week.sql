
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select day_of_week
from telegram_dw."raw_marts"."dim_dates"
where day_of_week is null



  
  
      
    ) dbt_internal_test