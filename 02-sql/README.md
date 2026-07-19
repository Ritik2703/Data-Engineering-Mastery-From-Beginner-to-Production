# 02 — SQL

All scenario queries are in [`all-scenarios-queries.sql`](./all-scenarios-queries.sql): window functions, dedup, SCD2 merge, gaps-and-islands, pivot, optimization, recursive CTEs.

## Indexing Strategy Cheat Sheet
- **B-Tree** (default) — equality & range queries, most common.
- **Hash** — equality-only lookups, faster than B-Tree for `=` but no range support.
- **Bitmap** — low-cardinality columns (gender, status flags) — common in warehouses (Oracle/Redshift).
- **Composite index** — order columns by: equality filters first, then range filters, then sort columns.
- **Covering index** — include all SELECTed columns so the engine never touches the base table.

## Query Optimization Flow
```
1. EXPLAIN ANALYZE the slow query
2. Check: Seq Scan on large table? → Add index
3. Check: Nested loop on huge join? → Rewrite as hash/merge join hint or add index on join key
4. Check: Sort spilling to disk? → Increase work_mem / add index matching ORDER BY
5. Re-run EXPLAIN ANALYZE → confirm improvement
```

## Common Interview Traps
- `WHERE` vs `HAVING` — WHERE filters rows before GROUP BY, HAVING filters after.
- `RANK()` vs `DENSE_RANK()` vs `ROW_NUMBER()` — ties handling differs.
- `INNER JOIN` silently drops NULLs — watch out for unintended row loss with LEFT JOIN + WHERE on right table column.

## Resources
- Mode SQL Tutorial: https://mode.com/sql-tutorial/
- Use The Index, Luke: https://use-the-index-luke.com/
- PostgreSQL EXPLAIN docs: https://www.postgresql.org/docs/current/using-explain.html
