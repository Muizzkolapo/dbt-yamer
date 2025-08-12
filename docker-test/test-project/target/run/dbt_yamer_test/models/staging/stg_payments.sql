
  create view "dbt_test_db"."dbt_yamer_test"."stg_payments__dbt_tmp"
    
    
  as (
    

select
    payment_id,
    order_id,
    payment_method,
    payment_status,
    amount_paid,
    payment_date,
    -- Categorize payment methods
    case
        when payment_method in ('credit_card', 'debit_card') then 'card'
        when payment_method = 'paypal' then 'digital_wallet'
        when payment_method = 'bank_transfer' then 'bank'
        else 'other'
    end as payment_type,
    -- Payment timing
    extract(hour from payment_date) as payment_hour
from "dbt_test_db"."dbt_yamer_test"."payments"
  );