
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select view_count
from telegram_dw."raw"."stg_telegram_messages"
where view_count is null



  
  
      
    ) dbt_internal_test