
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel_type
from telegram_dw."raw_marts"."dim_channels"
where channel_type is null



  
  
      
    ) dbt_internal_test