"""
AWS Data Engineering — boto3 cheat sheet
pip install boto3
"""
import boto3
import json

session = boto3.Session(region_name="ap-south-1")  # uses ~/.aws/credentials or IAM role

# ---------------- S3: upload / download / list ----------------
s3 = session.client("s3")

s3.upload_file("local_data.parquet", "my-data-lake-bucket", "raw/orders/2026/07/data.parquet")

s3.download_file("my-data-lake-bucket", "raw/orders/2026/07/data.parquet", "local_data.parquet")

objects = s3.list_objects_v2(Bucket="my-data-lake-bucket", Prefix="raw/orders/")
for obj in objects.get("Contents", []):
    print(obj["Key"], obj["Size"])

# ---------------- Glue: trigger an ETL job ----------------
glue = session.client("glue")

response = glue.start_job_run(
    JobName="orders-etl-job",
    Arguments={"--source_path": "s3://my-data-lake-bucket/raw/orders/",
               "--target_path": "s3://my-data-lake-bucket/curated/orders/"},
)
job_run_id = response["JobRunId"]
status = glue.get_job_run(JobName="orders-etl-job", RunId=job_run_id)
print(status["JobRun"]["JobRunState"])

# ---------------- Redshift: run a query via Data API (no persistent connection needed) ----------------
redshift_data = session.client("redshift-data")

exec_response = redshift_data.execute_statement(
    ClusterIdentifier="my-redshift-cluster",
    Database="dev",
    DbUser="awsuser",
    Sql="SELECT region, SUM(amount) FROM fact_sales GROUP BY region;",
)
statement_id = exec_response["Id"]
result = redshift_data.get_statement_result(Id=statement_id)
print(result["Records"])

# ---------------- Lambda: trigger a serverless transform function ----------------
lambda_client = session.client("lambda")

lambda_client.invoke(
    FunctionName="process-new-s3-file",
    InvocationType="Event",  # async
    Payload=json.dumps({"bucket": "my-data-lake-bucket", "key": "raw/orders/new_file.json"}),
)

# ---------------- Secrets Manager: pull DB credentials securely (never hardcode passwords) ----------------
secrets = session.client("secretsmanager")
secret_value = json.loads(secrets.get_secret_value(SecretId="prod/redshift/creds")["SecretString"])
db_password = secret_value["password"]
