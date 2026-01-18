
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select has_media
from telegram_dw."raw"."stg_telegram_messages"
where has_media is null



  
  
      
    ) dbt_internal_test