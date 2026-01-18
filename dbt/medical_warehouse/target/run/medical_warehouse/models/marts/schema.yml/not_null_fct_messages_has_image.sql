
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select has_image
from telegram_dw."raw_marts"."fct_messages"
where has_image is null



  
  
      
    ) dbt_internal_test