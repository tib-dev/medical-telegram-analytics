
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select month_name
from telegram_dw."raw_marts"."dim_dates"
where month_name is null



  
  
      
    ) dbt_internal_test