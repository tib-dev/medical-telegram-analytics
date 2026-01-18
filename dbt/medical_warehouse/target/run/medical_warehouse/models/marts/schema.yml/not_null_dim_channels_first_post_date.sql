
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select first_post_date
from telegram_dw."raw_marts"."dim_channels"
where first_post_date is null



  
  
      
    ) dbt_internal_test