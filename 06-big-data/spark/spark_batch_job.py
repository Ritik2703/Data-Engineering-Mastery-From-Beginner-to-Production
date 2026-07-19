"""
Spark batch job: read raw sales data from S3/ADLS, clean, aggregate, write partitioned Parquet.
Run: spark-submit spark_batch_job.py
"""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = (
    SparkSession.builder
    .appName("sales-daily-aggregation")
    .config("spark.sql.shuffle.partitions", "200")
    .getOrCreate()
)

# 1. Extract
raw_df = spark.read.option("header", True).option("inferSchema", True) \
    .parquet("s3a://data-lake/raw/sales/")

# 2. Clean / Transform
clean_df = (
    raw_df
    .dropDuplicates(["transaction_id"])
    .filter(F.col("amount") > 0)
    .withColumn("sale_date", F.to_date("transaction_ts"))
    .withColumn("amount", F.col("amount").cast("double"))
)

# 3. Deduplicate keeping latest record per key (common CDC scenario)
window_spec = Window.partitionBy("transaction_id").orderBy(F.col("transaction_ts").desc())
deduped_df = (
    clean_df.withColumn("rn", F.row_number().over(window_spec))
    .filter(F.col("rn") == 1)
    .drop("rn")
)

# 4. Aggregate
daily_summary = (
    deduped_df.groupBy("sale_date", "region", "product_category")
    .agg(
        F.sum("amount").alias("total_sales"),
        F.count("transaction_id").alias("num_transactions"),
        F.avg("amount").alias("avg_ticket_size"),
    )
)

# 5. Load — partitioned write for efficient downstream querying
(
    daily_summary.write
    .mode("overwrite")
    .partitionBy("sale_date")
    .parquet("s3a://data-lake/curated/daily_sales_summary/")
)

print("Job completed:", daily_summary.count(), "aggregated rows written")
spark.stop()
