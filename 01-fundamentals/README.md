# 01 — Fundamentals

## OLTP vs OLAP

| | OLTP | OLAP |
|---|---|---|
| Purpose | Transaction processing | Analysis/reporting |
| Schema | Normalized (3NF) | Denormalized (Star/Snowflake) |
| Examples | App DB (orders, users) | Data warehouse (Snowflake, BigQuery) |
| Query type | Short, frequent writes | Complex, large reads |

## Star Schema vs Snowflake Schema

**Star Schema** — one fact table, denormalized dimension tables (fast, simple joins):
```
        dim_customer
             │
dim_date ─ fact_sales ─ dim_product
             │
         dim_store
```

**Snowflake Schema** — dimensions further normalized into sub-dimensions (saves space, more joins):
```
dim_customer ── dim_city ── dim_country
       │
   fact_sales
```

## Data Modeling Approaches
- **Kimball (bottom-up)** — build dimensional marts per business process, conform dimensions later. Fast to deliver value.
- **Inmon (top-down)** — build normalized enterprise DW first, then marts. More consistent, slower to start.
- **Data Vault** — Hubs (business keys), Links (relationships), Satellites (attributes/history). Great for auditability & fast-changing sources.
- **One Big Table (OBT)** — modern lakehouse pattern; pre-join everything into one wide table for BI simplicity at query time.

## Slowly Changing Dimensions (SCD)
- **Type 0** — never update (fixed).
- **Type 1** — overwrite old value (no history).
- **Type 2** — add new row with version/effective dates (full history) — most common in interviews.
- **Type 3** — add a new column for previous value (limited history).

### SCD Type 2 example (SQL)
```sql
-- Close old record
UPDATE dim_customer
SET end_date = CURRENT_DATE, is_current = FALSE
WHERE customer_id = 101 AND is_current = TRUE;

-- Insert new version
INSERT INTO dim_customer (customer_id, name, city, start_date, end_date, is_current)
VALUES (101, 'Rahul Sharma', 'Bangalore', CURRENT_DATE, NULL, TRUE);
```

## ETL vs ELT
- **ETL**: Extract → Transform (in staging server) → Load into warehouse. Used with legacy tools (SSIS, Informatica) where warehouse compute was expensive/limited.
- **ELT**: Extract → Load raw → Transform inside the warehouse (Snowflake/BigQuery compute). Modern default because cloud warehouses are cheap & scalable; enables tools like **dbt**.

## Data Warehouse vs Data Lake vs Lakehouse
- **Warehouse**: structured, schema-on-write, fast SQL analytics (Snowflake, Redshift, BigQuery).
- **Lake**: raw files (any format), schema-on-read, cheap storage (S3, ADLS, GCS).
- **Lakehouse**: lake storage + warehouse-like transactions/schema via Delta Lake / Iceberg / Hudi — best of both.

See `resources.md` for further reading links.
