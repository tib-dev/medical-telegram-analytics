
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select month
from telegram_dw."raw_marts"."dim_dates"
where month is null



  
  
      
    ) dbt_internal_test