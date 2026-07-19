# Azure for Data Engineering

## Typical Azure Data Pipeline
```
Sources (on-prem SQL, SaaS APIs, Microsoft 365/Graph API)
        │  Azure Data Factory (ADF) — orchestration + copy activities
        ▼
   ADLS Gen2 (raw zone — hierarchical namespace, S3-equivalent)
        │  Databricks (Spark) or Synapse Spark Pools — transform
        ▼
   ADLS Gen2 (curated zone) ── or ── Synapse Analytics (SQL pool)
        │
        ▼
   Power BI (native, best integration in Azure ecosystem)
```

## Key Services
| Service | Purpose |
|---|---|
| **Azure Data Factory (ADF)** | Orchestration + data movement (like Airflow + Glue combined), drag-drop pipelines |
| **ADLS Gen2** | Data lake storage (blob storage + hierarchical namespace) |
| **Azure Databricks** | Managed Spark — most common heavy transform engine in Azure shops |
| **Synapse Analytics** | Unified: SQL pools (warehouse) + Spark pools + pipelines in one workspace |
| **Azure SQL Database / Managed Instance** | OLTP, PaaS SQL Server |
| **Microsoft Graph API** | Pull data from Microsoft 365 — Users (Azure AD), SharePoint, Teams, Outlook, OneDrive |
| **Event Hubs** | Managed streaming ingestion (Kafka-compatible endpoint available) |
| **Key Vault** | Secure secrets/credentials storage |

## Microsoft Graph API — why it matters for DE
Many enterprises need to pull org data (users, groups, licenses), collaboration data (Teams messages/meetings for analytics), or SharePoint list data (used as makeshift business databases by non-technical teams) into the warehouse. Graph API is the **single unified endpoint** for all Microsoft 365 data.

See [`microsoft_graph_api_pull.py`](./microsoft_graph_api_pull.py) for:
- OAuth2 client-credentials auth (unattended/scheduled pipeline pattern)
- Pagination handling (`@odata.nextLink`)
- Pulling Users, SharePoint list items, Teams channel messages

## ADF Pipeline Concepts (drag-drop, but good to know the JSON underneath)
- **Linked Service** = connection string/credentials to a source or sink
- **Dataset** = pointer to a specific table/file within a linked service
- **Pipeline** = sequence of Activities (Copy, Data Flow, Stored Procedure, Databricks Notebook)
- **Trigger** = schedule (time-based) or event-based (e.g., file arrival in ADLS)
- **Integration Runtime** = compute that executes the activity (Azure IR for cloud, Self-hosted IR for on-prem sources)

## Resources
- Microsoft Graph API docs: https://learn.microsoft.com/en-us/graph/overview
- ADF docs: https://learn.microsoft.com/en-us/azure/data-factory/
