
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select forward_count
from telegram_dw."raw"."stg_telegram_messages"
where forward_count is null



  
  
      
    ) dbt_internal_test