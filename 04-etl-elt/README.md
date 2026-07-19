# 04 — ETL / ELT

## Flow: Legacy ETL vs Modern ELT

**Legacy ETL (SSIS / Informatica / Talend):**
```
Source DB → Staging Server (transform: cleanse, join, dedupe) → Load into DW
              (transform happens OUTSIDE the warehouse, on ETL server compute)
```

**Modern ELT (Airflow + dbt):**
```
Source (API/DB/files) → Raw load into Warehouse/Lake (S3, Snowflake, BigQuery)
                       → Transform IN warehouse using SQL (dbt models)
                       → Curated tables for BI
```

## Files
- [`airflow/etl_dag_example.py`](./airflow/etl_dag_example.py) — full DAG: extract → transform → load → DQ check
- [`dbt_example/models_example.sql`](./dbt_example/models_example.sql) — staging + mart models with tests

## Legacy Tools — Quick Notes (still asked in interviews for enterprise roles)
- **SSIS (SQL Server Integration Services)**: drag-drop control flow + data flow tasks; common in Microsoft shops.
- **Informatica PowerCenter**: mapping-based ETL, strong in banking/insurance; separates Source/Target/Transformation objects.
- **Talend**: Java-code-generating ETL tool, open-source + enterprise editions.

## Modern Tools
- **Airflow**: orchestration (schedules and monitors tasks, doesn't do heavy transforms itself).
- **dbt**: transformation layer — "SQL + software engineering practices" (version control, tests, docs, lineage).
- **Fivetran / Airbyte**: managed EL (extract-load) connectors — reduces custom extraction code.

## Data Quality Checks (add to every pipeline)
1. Row count sanity (not zero, not wildly different from historical average)
2. Null checks on critical columns (primary keys, foreign keys)
3. Uniqueness checks on primary keys
4. Freshness check (data updated within expected SLA window)
5. Schema drift detection (new/missing columns from source)

## Resources
- dbt docs: https://docs.getdbt.com/
- Airflow docs: https://airflow.apache.org/docs/
