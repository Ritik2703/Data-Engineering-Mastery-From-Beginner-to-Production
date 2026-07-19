"""
GCP Data Engineering — BigQuery cheat sheet
pip install google-cloud-bigquery google-cloud-storage
"""
from google.cloud import bigquery
from google.cloud import storage

client = bigquery.Client(project="my-gcp-project")

# ---------------- Load data from GCS into BigQuery ----------------
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition="WRITE_APPEND",
)
load_job = client.load_table_from_uri(
    "gs://my-data-lake-bucket/raw/orders/*.parquet",
    "my-gcp-project.analytics.raw_orders",
    job_config=job_config,
)
load_job.result()  # wait for completion
print(f"Loaded {load_job.output_rows} rows")

# ---------------- Query BigQuery (pay-per-TB-scanned) ----------------
query = """
    SELECT region, DATE_TRUNC(order_date, MONTH) AS month, SUM(amount) AS total_sales
    FROM `my-gcp-project.analytics.fct_orders`
    WHERE order_date >= '2026-01-01'
    GROUP BY region, month
    ORDER BY month
"""
df = client.query(query).to_dataframe()
print(df.head())

# ---------------- Create a partitioned + clustered table (cost optimization) ----------------
schema = [
    bigquery.SchemaField("order_id", "STRING"),
    bigquery.SchemaField("order_date", "DATE"),
    bigquery.SchemaField("region", "STRING"),
    bigquery.SchemaField("amount", "NUMERIC"),
]
table = bigquery.Table("my-gcp-project.analytics.fct_orders_optimized", schema=schema)
table.time_partitioning = bigquery.TimePartitioning(field="order_date")
table.clustering_fields = ["region"]
client.create_table(table)

# ---------------- Upload local file to GCS (common pre-load step) ----------------
storage_client = storage.Client()
bucket = storage_client.bucket("my-data-lake-bucket")
blob = bucket.blob("raw/orders/2026-07-19.parquet")
blob.upload_from_filename("local_data.parquet")
