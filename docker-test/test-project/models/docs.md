{% docs col_customer_id %}
Unique identifier for each customer in the system. This is the primary key for customer records.
{% enddocs %}

{% docs col_full_name %}
The customer's complete name, concatenated from first_name and last_name fields.
{% enddocs %}

{% docs col_email %}
Customer's email address used for communication and account identification.
{% enddocs %}

{% docs col_customer_status %}
Current status of the customer account. Values include: active, inactive, pending.
{% enddocs %}

{% docs col_registration_date %}
The date when the customer first registered their account.
{% enddocs %}

{% docs col_order_id %}
Unique identifier for each order placed in the system.
{% enddocs %}

{% docs col_order_date %}
The date when the order was placed by the customer.
{% enddocs %}

{% docs col_order_status %}
Current status of the order. Values include: completed, pending, processing, cancelled.
{% enddocs %}

{% docs col_total_amount %}
The total monetary value of the order including all items and fees.
{% enddocs %}

{% docs col_payment_method %}
The method used for payment. Values include: credit_card, debit_card, paypal, bank_transfer.
{% enddocs %}

{% docs col_payment_status %}
Current status of the payment. Values include: completed, pending, failed.
{% enddocs %}

{% docs col_amount_paid %}
The actual amount that was paid for this transaction.
{% enddocs %}

{% docs col_dim_customers_customer_segment %}
Customer segmentation based on spending behavior: high_value, medium_value, low_value, no_purchase.
{% enddocs %}

{% docs col_dim_customers_lifecycle_status %}
Customer lifecycle stage: prospect, first_time, active, at_risk, inactive.
{% enddocs %}

{% docs col_fct_orders_order_size %}
Categorization of order by monetary value: large, medium, small.
{% enddocs %}

{% docs col_fct_orders_days_to_payment %}
Number of days between order placement and payment completion.
{% enddocs %}

{% docs stg_customers %}
Staging table for customer data with basic transformations and derived fields.
{% enddocs %}

{% docs stg_orders %}
Staging table for order data with status categorization and date extractions.
{% enddocs %}

{% docs stg_payments %}
Staging table for payment data with payment type categorization.
{% enddocs %}

{% docs dim_customers %}
Customer dimension table with segmentation and lifecycle analysis.
{% enddocs %}

{% docs fct_orders %}
Orders fact table combining order, customer, and payment information.
{% enddocs %}