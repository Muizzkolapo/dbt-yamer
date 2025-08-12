

select
    customer_id,
    full_name,
    email,
    customer_status,
    registration_date,
    total_orders,
    completed_orders,
    total_spent,
    avg_order_value,
    last_order_date,
    first_order_date,
    -- Customer segments
    case
        when total_spent >= 500 then 'high_value'
        when total_spent >= 200 then 'medium_value'
        when total_spent > 0 then 'low_value'
        else 'no_purchase'
    end as customer_segment,
    -- Customer lifecycle
    case
        when total_orders = 0 then 'prospect'
        when total_orders = 1 then 'first_time'
        when last_order_date >= current_date - interval '30 days' then 'active'
        when last_order_date >= current_date - interval '90 days' then 'at_risk'
        else 'inactive'
    end as lifecycle_status,
    -- Metrics
    case 
        when first_order_date is not null then 
            last_order_date - first_order_date 
        else null 
    end as customer_lifetime_days
from "dbt_test_db"."dbt_yamer_test"."int_customer_orders"