# 12 — Interview Prep

## SQL Questions
1. Find the 2nd/Nth highest salary per department. *(see `02-sql/all-scenarios-queries.sql`)*
2. Find customers who ordered in every month of the year (all-months pattern — use `COUNT(DISTINCT month) = 12`).
3. Detect duplicate rows and remove them keeping the latest.
4. Write a query to find consecutive login streaks (gaps & islands).
5. Difference between `RANK()`, `DENSE_RANK()`, `ROW_NUMBER()` — give an example where results differ.
6. Explain `WHERE` vs `HAVING` vs `QUALIFY` (Snowflake-specific).
7. Write a self-join to find employees who earn more than their manager.
8. Explain index types and when a query would NOT use an available index.

## Python Questions
1. Difference between a list, tuple, set, and dict — time complexity of lookups.
2. How would you process a file too large to fit in memory? (chunking with pandas `chunksize`, or generators)
3. Write a function to deduplicate a list of dicts by a key, keeping the latest by timestamp.
4. Explain `*args`, `**kwargs`, decorators, and generators with a data pipeline example (e.g., a retry decorator).
5. How do you handle API rate limits in a Python extraction script? (exponential backoff, `tenacity`, sleep between calls)
6. Multiprocessing vs multithreading vs asyncio — which for I/O-bound API calls? (asyncio or threading — GIL released during I/O wait)

## ETL / Data Modeling Questions
1. Explain SCD Type 1 vs 2 vs 3 with an example.
2. ETL vs ELT — when would you pick one over the other?
3. How do you design a pipeline to be idempotent (safe to re-run)?
4. How do you handle schema evolution (new column appears in source)?
5. Star schema vs Data Vault — tradeoffs for a fast-changing source system.
6. How would you implement incremental loading from a source with no `updated_at` column? (CDC via binlog/WAL, or full snapshot diff)

## System Design Questions
1. Design a data pipeline to ingest IoT sensor data at 1M events/sec.
2. Design a near-real-time fraud detection pipeline for a payments company.
3. Design a data warehouse for a multi-country e-commerce company (currency, timezone, locale considerations).
4. How would you migrate a legacy on-prem SSIS/Informatica ETL suite to a cloud-native stack?
5. How do you monitor pipeline health and alert on failures/SLA breaches at scale (100s of DAGs)?

## Behavioral (common for DE roles)
1. Tell me about a time a pipeline failed in production — how did you debug and fix it?
2. Describe a time you had to push back on unrealistic data requirements/timelines.
3. How do you handle disagreements with a data analyst about a metric definition?
4. Tell me about the most complex data pipeline you've built end-to-end.

> Tip: for every answer, use the **STAR format** (Situation, Task, Action, Result) and quantify impact where possible (e.g., "reduced pipeline runtime by 40%", "cut cloud costs by $2k/month via partition pruning").
