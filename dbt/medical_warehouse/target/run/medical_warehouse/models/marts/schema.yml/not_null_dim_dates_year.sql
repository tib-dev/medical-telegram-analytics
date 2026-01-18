
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select year
from telegram_dw."raw_marts"."dim_dates"
where year is null



  
  
      
    ) dbt_internal_test