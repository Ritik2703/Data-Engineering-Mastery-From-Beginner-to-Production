# GCP for Data Engineering

## Typical GCP Pipeline
```
Sources → Cloud Storage (GCS, raw zone) → Dataflow (Apache Beam, batch/stream)
        → BigQuery (curated, serverless DW) → Looker / Power BI / Tableau
        Orchestrated by Cloud Composer (managed Airflow)
```

## Key Services
| Service | Purpose |
|---|---|
| **BigQuery** | Serverless data warehouse, pay-per-query, extremely fast on huge scans |
| **Cloud Storage (GCS)** | Object storage — data lake |
| **Dataflow** | Managed Apache Beam — unified batch + streaming processing |
| **Cloud Composer** | Managed Airflow |
| **Pub/Sub** | Managed messaging (Kafka-equivalent) |
| **Dataproc** | Managed Hadoop/Spark clusters |
| **Looker** | Native GCP BI tool (also LookML semantic layer) |

See [`bigquery_examples.py`](./bigquery_examples.py) for load jobs, partitioned/clustered tables, GCS upload.

---

# ☁️ Cross-Cloud Comparison (AWS vs Azure vs GCP)

| Concept | AWS | Azure | GCP |
|---|---|---|---|
| Object Storage | S3 | ADLS Gen2 / Blob Storage | Cloud Storage (GCS) |
| Data Warehouse | Redshift | Synapse Analytics | BigQuery |
| Managed Spark | EMR / Glue | Databricks / Synapse Spark | Dataproc |
| Serverless ETL | Glue | ADF Mapping Data Flows | Dataflow (Beam) |
| Orchestration | Step Functions / MWAA | ADF / Azure Functions | Cloud Composer |
| Streaming | Kinesis | Event Hubs | Pub/Sub |
| Serverless SQL on lake | Athena | Synapse Serverless SQL | BigQuery (native) |
| Secrets | Secrets Manager | Key Vault | Secret Manager |
| BI Tool (native) | QuickSight | Power BI | Looker |

**Rule of thumb:** most companies pick their cloud based on existing enterprise agreements (Microsoft shops → Azure, general/startups → AWS, ML/analytics-heavy or Google Workspace shops → GCP). Concepts transfer 90% across clouds — only service names and SDKs differ.
