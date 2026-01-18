
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message_date
from telegram_dw."raw"."stg_telegram_messages"
where message_date is null



  
  
      
    ) dbt_internal_test