{{ config(materialized='view') }}

select
    c.customer_id,
    c.full_name,
    c.email,
    c.customer_status,
    c.registration_date,
    -- Order metrics
    count(o.order_id) as total_orders,
    count(case when o.order_status = 'completed' then 1 end) as completed_orders,
    coalesce(sum(case when o.order_status = 'completed' then o.total_amount end), 0) as total_spent,
    coalesce(avg(case when o.order_status = 'completed' then o.total_amount end), 0) as avg_order_value,
    max(o.order_date) as last_order_date,
    min(o.order_date) as first_order_date
from {{ ref('stg_customers') }} c
left join {{ ref('stg_orders') }} o on c.customer_id = o.customer_id
group by 1, 2, 3, 4, 5