

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    o.order_category,
    o.total_amount,
    o.order_year,
    o.order_month,
    o.order_quarter,
    -- Customer information
    c.full_name as customer_name,
    c.customer_segment,
    c.lifecycle_status,
    -- Payment information
    p.payment_method,
    p.payment_type,
    p.payment_status,
    p.amount_paid,
    p.payment_date,
    -- Calculated fields
    case 
        when o.total_amount > 200 then 'large'
        when o.total_amount > 100 then 'medium'
        else 'small'
    end as order_size,
    -- Time to payment
    case
        when p.payment_date is not null and o.order_date is not null then
            p.payment_date - o.order_date
        else null
    end as days_to_payment
from "dbt_test_db"."dbt_yamer_test"."stg_orders" o
left join "dbt_test_db"."dbt_yamer_test"."dim_customers" c on o.customer_id = c.customer_id
left join "dbt_test_db"."dbt_yamer_test"."stg_payments" p on o.order_id = p.order_id