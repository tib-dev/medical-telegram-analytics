
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select quarter
from telegram_dw."raw_marts"."dim_dates"
where quarter is null



  
  
      
    ) dbt_internal_test