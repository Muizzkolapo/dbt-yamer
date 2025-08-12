

select
    order_id,
    customer_id,
    order_date,
    order_status,
    total_amount,
    -- Derived fields
    case
        when order_status = 'completed' then 'fulfilled'
        when order_status in ('pending', 'processing') then 'in_progress'
        when order_status = 'cancelled' then 'cancelled'
        else 'unknown'
    end as order_category,
    -- Date calculations
    extract(year from order_date) as order_year,
    extract(month from order_date) as order_month,
    extract(quarter from order_date) as order_quarter
from "dbt_test_db"."dbt_yamer_test"."orders"