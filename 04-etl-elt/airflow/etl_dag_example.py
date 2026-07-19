"""
Example Airflow DAG: API -> S3 (raw) -> Spark transform -> Snowflake (curated) -> Slack alert on failure
pip install apache-airflow
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.sensors.filesystem import FileSensor

default_args = {
    "owner": "data-eng-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["data-eng-alerts@company.com"],
}

with DAG(
    dag_id="orders_pipeline_daily",
    default_args=default_args,
    description="Extract orders API -> S3 -> transform -> Snowflake",
    schedule_interval="0 2 * * *",   # every day at 2 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "orders", "daily"],
) as dag:

    def extract_from_api(**context):
        from api_to_db.rest_api_to_postgres import fetch_page  # reuse extraction logic
        # ... pull data, write raw json/parquet to S3 ...
        print("Extracted data to S3 raw zone")

    def transform_with_spark(**context):
        # spark-submit or call a PySpark job here
        print("Transformed raw -> curated with Spark")

    def load_to_snowflake(**context):
        # COPY INTO from S3 stage, or use snowflake-connector-python
        print("Loaded curated data into Snowflake")

    def data_quality_check(**context):
        # Row count check, null check, freshness check
        row_count = 12345  # placeholder for actual check query result
        if row_count == 0:
            raise ValueError("Data quality check failed: 0 rows loaded")
        print(f"DQ check passed: {row_count} rows")

    t1_extract = PythonOperator(task_id="extract_from_api", python_callable=extract_from_api)
    t2_transform = PythonOperator(task_id="transform_with_spark", python_callable=transform_with_spark)
    t3_load = PythonOperator(task_id="load_to_snowflake", python_callable=load_to_snowflake)
    t4_dq_check = PythonOperator(task_id="data_quality_check", python_callable=data_quality_check)

    # Dependency chain
    t1_extract >> t2_transform >> t3_load >> t4_dq_check
