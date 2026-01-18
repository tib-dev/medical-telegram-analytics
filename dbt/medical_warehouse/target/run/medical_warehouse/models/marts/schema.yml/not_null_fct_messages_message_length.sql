
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message_length
from telegram_dw."raw_marts"."fct_messages"
where message_length is null



  
  
      
    ) dbt_internal_test