-- ============================================================
-- dbt project layout convention:
-- models/staging/stg_orders.sql   -> clean + rename raw source
-- models/marts/fct_orders.sql     -> business logic / fact table
-- ============================================================

-- models/staging/stg_orders.sql
-- {{ config(materialized='view') }}
SELECT
    order_id,
    customer_id,
    CAST(amount AS NUMERIC(10,2)) AS amount,
    LOWER(TRIM(status)) AS status,
    CAST(updated_at AS TIMESTAMP) AS updated_at
FROM {{ source('raw', 'orders') }}
WHERE order_id IS NOT NULL;


-- models/marts/fct_orders.sql
-- {{ config(materialized='table') }}
WITH stg AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
customers AS (
    SELECT * FROM {{ ref('dim_customer') }}
)
SELECT
    stg.order_id,
    stg.customer_id,
    customers.customer_segment,
    stg.amount,
    stg.status,
    stg.updated_at
FROM stg
LEFT JOIN customers ON stg.customer_id = customers.customer_id;


-- schema.yml (tests — dbt's built-in data quality framework)
-- version: 2
-- models:
--   - name: fct_orders
--     columns:
--       - name: order_id
--         tests: [unique, not_null]
--       - name: status
--         tests:
--           - accepted_values:
--               values: ['pending', 'completed', 'cancelled']

-- Run:
--   dbt run          -> builds models
--   dbt test         -> runs data quality tests
--   dbt docs generate -> builds lineage graph docs
