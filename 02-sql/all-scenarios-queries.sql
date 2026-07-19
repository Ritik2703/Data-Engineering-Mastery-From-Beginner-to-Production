-- ============================================================
-- 02-SQL : ALL SCENARIOS CHEAT SHEET
-- ============================================================

-- ---------- 1. WINDOW FUNCTIONS ----------

-- Running total of sales per customer, ordered by date
SELECT
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM orders;

-- Rank customers by total spend (dense_rank handles ties without gaps)
SELECT
    customer_id,
    SUM(amount) AS total_spend,
    DENSE_RANK() OVER (ORDER BY SUM(amount) DESC) AS spend_rank
FROM orders
GROUP BY customer_id;

-- Find 2nd highest salary per department (classic interview Q)
SELECT department_id, salary
FROM (
    SELECT department_id, salary,
           DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk = 2;

-- Month-over-month growth using LAG
SELECT
    month,
    revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) AS mom_change,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
          / LAG(revenue) OVER (ORDER BY month), 2) AS mom_growth_pct
FROM monthly_revenue;

-- ---------- 2. DEDUPLICATION (very common ETL scenario) ----------

-- Remove duplicate rows keeping the latest record per key
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated_at DESC) AS rn
    FROM customers_raw
)
SELECT * FROM ranked WHERE rn = 1;

-- ---------- 3. SCD TYPE 2 MERGE (upsert with history) ----------
MERGE INTO dim_customer AS target
USING staging_customer AS source
ON target.customer_id = source.customer_id AND target.is_current = TRUE
WHEN MATCHED AND (target.city <> source.city OR target.name <> source.name) THEN
    UPDATE SET target.end_date = CURRENT_DATE, target.is_current = FALSE
WHEN NOT MATCHED THEN
    INSERT (customer_id, name, city, start_date, end_date, is_current)
    VALUES (source.customer_id, source.name, source.city, CURRENT_DATE, NULL, TRUE);

-- ---------- 4. GAPS & ISLANDS (detect consecutive login streaks) ----------
WITH numbered AS (
    SELECT user_id, login_date,
           login_date - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date))::int AS grp
    FROM user_logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_len
FROM numbered
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;

-- ---------- 5. PIVOT (rows to columns) ----------
SELECT
    product_id,
    SUM(CASE WHEN quarter = 'Q1' THEN sales END) AS Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN sales END) AS Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN sales END) AS Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN sales END) AS Q4
FROM quarterly_sales
GROUP BY product_id;

-- ---------- 6. QUERY OPTIMIZATION CHECKLIST ----------
-- a) Use EXPLAIN / EXPLAIN ANALYZE before optimizing blindly
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 101;

-- b) Index the columns used in WHERE / JOIN / ORDER BY
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- c) Avoid SELECT * in production pipelines — pull only needed columns
-- d) Avoid functions on indexed columns in WHERE (kills index usage)
--    Bad:  WHERE YEAR(order_date) = 2026
--    Good: WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'

-- e) Use covering indexes for read-heavy reporting queries
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date) INCLUDE (amount);

-- f) Partition large fact tables by date for pruning
CREATE TABLE fact_sales (
    sale_id BIGINT,
    sale_date DATE,
    amount NUMERIC
) PARTITION BY RANGE (sale_date);

-- ---------- 7. CTE vs SUBQUERY vs TEMP TABLE ----------
-- CTE: readability, single-use, not materialized in most engines (except recursive)
-- Subquery: fine for simple filters, gets messy nested
-- Temp table: use when reusing intermediate result multiple times / large data

-- Recursive CTE example — org hierarchy
WITH RECURSIVE org_chart AS (
    SELECT employee_id, manager_id, name, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, e.name, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT * FROM org_chart ORDER BY level;
