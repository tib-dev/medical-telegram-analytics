
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    channel_name as unique_field,
    count(*) as n_records

from telegram_dw."raw_marts"."dim_channels"
where channel_name is not null
group by channel_name
having count(*) > 1



  
  
      
    ) dbt_internal_test