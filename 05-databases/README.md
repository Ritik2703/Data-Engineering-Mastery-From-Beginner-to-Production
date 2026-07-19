# 05 — Databases

Connection code examples already covered in [`03-python/api-to-db/db_connect_examples.py`](../03-python/api-to-db/db_connect_examples.py). This section covers **when to use what**.

## Relational (OLTP)
| DB | Best For | Notes |
|---|---|---|
| PostgreSQL | General purpose, JSONB support | Open-source favorite, great extensions (PostGIS) |
| MySQL | Web apps | Simpler, huge community |
| SQL Server | Microsoft-stack enterprises | Strong with SSIS/Power BI integration |
| Oracle | Legacy large enterprises (banking) | Expensive licensing, very mature |

## NoSQL
| DB | Type | Best For |
|---|---|---|
| MongoDB | Document | Flexible schema, nested JSON data |
| Cassandra | Wide-column | High write throughput, multi-datacenter |
| DynamoDB | Key-value/Document | Serverless AWS-native, single-digit ms latency |
| Redis | In-memory KV | Caching, session store, real-time counters |

## Data Warehouses (OLAP / Cloud-native)
| DW | Cloud | Pricing Model | Notes |
|---|---|---|---|
| Snowflake | Multi-cloud | Compute (per-second) + storage separate | Best-in-class separation of storage/compute |
| BigQuery | GCP | Pay-per-query (per TB scanned) or flat-rate | Serverless, no cluster management |
| Redshift | AWS | Cluster-based (or Serverless) | Deep AWS ecosystem integration |
| Synapse Analytics | Azure | Cluster/serverless | Combines DW + Spark in one workspace |

## Data Lakes / Lakehouse formats
- **Delta Lake** (Databricks) — ACID transactions on top of Parquet, time travel.
- **Apache Iceberg** — open table format, strong multi-engine support (Spark, Trino, Flink).
- **Apache Hudi** — optimized for upserts/incremental pulls (CDC use cases).

## Choosing a database — quick decision guide
```
Need transactional writes + relationships?      -> Relational (Postgres/MySQL)
Need flexible/nested schema, high write speed?  -> MongoDB / Cassandra
Need sub-ms lookups, serverless scaling?         -> DynamoDB / Redis
Need to run analytics on billions of rows?       -> Snowflake / BigQuery / Redshift
Need cheap raw storage + multiple engines?       -> Data Lake + Iceberg/Delta
```
