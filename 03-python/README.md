# 03 — Python for Data Engineering

## Files
- [`api-to-db/rest_api_to_postgres.py`](./api-to-db/rest_api_to_postgres.py) — paginated API pull with retry, incremental watermark, bulk upsert
- [`api-to-db/db_connect_examples.py`](./api-to-db/db_connect_examples.py) — connection snippets for Postgres, MySQL, MongoDB, Snowflake, Oracle, Redshift, SQL Server

## Pandas — Common ETL Operations
```python
import pandas as pd

df = pd.read_csv("orders.csv")

# Clean
df = df.drop_duplicates(subset=["order_id"])
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df = df.dropna(subset=["amount"])

# Transform
df["order_month"] = pd.to_datetime(df["order_date"]).dt.to_period("M")
summary = df.groupby(["order_month", "region"])["amount"].sum().reset_index()

# Merge (like SQL join)
customers = pd.read_csv("customers.csv")
merged = df.merge(customers, on="customer_id", how="left")

# Load
merged.to_parquet("output/orders_enriched.parquet", index=False)
```

## PySpark — Distributed Processing
```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("etl-job").getOrCreate()

df = spark.read.option("header", True).csv("s3a://bucket/raw/orders/")

cleaned = (
    df.dropDuplicates(["order_id"])
      .withColumn("amount", F.col("amount").cast("double"))
      .filter(F.col("amount").isNotNull())
)

agg = (
    cleaned.groupBy("region", F.date_trunc("month", "order_date").alias("month"))
           .agg(F.sum("amount").alias("total_sales"))
)

agg.write.mode("overwrite").partitionBy("month").parquet("s3a://bucket/curated/sales_summary/")
```

## Why Python for DE?
- Glue code between every system: APIs, DBs, cloud SDKs (boto3, azure-sdk, google-cloud)
- pandas → in-memory transforms (small-medium data)
- PySpark → distributed transforms (big data)
- Airflow/dbt/Dagster are all Python-based orchestration

## Resources
- Real Python: https://realpython.com/
- PySpark docs: https://spark.apache.org/docs/latest/api/python/
