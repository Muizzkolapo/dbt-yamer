{{ config(materialized='view') }}

select
    customer_id,
    first_name,
    last_name,
    email,
    registration_date,
    customer_status,
    -- Derived fields
    concat(first_name, ' ', last_name) as full_name,
    case 
        when customer_status = 'active' then true
        else false
    end as is_active,
    -- Date calculations
    current_date - registration_date as days_since_registration
from {{ ref('customers') }}