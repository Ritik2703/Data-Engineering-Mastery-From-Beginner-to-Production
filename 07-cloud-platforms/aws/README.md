# AWS for Data Engineering

## Typical AWS Data Pipeline
```
Sources (APIs, on-prem DB, apps)
        │  (CDC via DMS, or custom scripts)
        ▼
   S3 (raw zone)
        │  Glue Crawler (infers schema) → Glue Data Catalog
        ▼
   Glue ETL Job / EMR (Spark) — transform
        ▼
   S3 (curated zone) ── or ── Redshift (COPY command)
        │
        ▼
   Athena (serverless SQL on S3) / QuickSight / Power BI / Tableau
```

## Key Services
| Service | Purpose |
|---|---|
| **S3** | Object storage — data lake foundation |
| **Glue** | Serverless ETL (Spark under the hood) + Data Catalog (metastore) |
| **EMR** | Managed Hadoop/Spark clusters — for heavier custom big-data jobs |
| **Redshift** | Cloud data warehouse |
| **Athena** | Serverless SQL queries directly on S3 (pay per TB scanned) |
| **Lambda** | Serverless functions — event-driven micro-transforms (e.g., on S3 file arrival) |
| **Kinesis** | Managed streaming (Kafka alternative, AWS-native) |
| **Step Functions** | Orchestrate Lambda/Glue/EMR workflows (AWS-native alternative to Airflow) |
| **DMS** | Database Migration Service — CDC replication from on-prem/RDS to S3/Redshift |
| **Secrets Manager** | Secure credential storage (never hardcode DB passwords) |

## Code
See [`boto3_examples.py`](./boto3_examples.py) for S3 upload/download, Glue job trigger, Redshift Data API query, Lambda invoke, Secrets Manager.

## IAM Best Practice
Always use **least-privilege IAM roles** attached to Glue/Lambda/EC2 — avoid hardcoded access keys in code/pipelines wherever possible.
