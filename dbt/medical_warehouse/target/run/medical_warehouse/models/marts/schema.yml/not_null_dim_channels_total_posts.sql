
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_posts
from telegram_dw."raw_marts"."dim_channels"
where total_posts is null



  
  
      
    ) dbt_internal_test