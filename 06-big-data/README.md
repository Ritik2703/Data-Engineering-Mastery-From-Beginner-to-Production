# 06 — Big Data

## Hadoop Ecosystem (Legacy but still in many enterprises)
```
HDFS (storage) ── MapReduce (processing, largely replaced by Spark) ── YARN (resource mgmt)
                              │
                     Hive (SQL-on-Hadoop) ── HBase (NoSQL on HDFS)
```
- **HDFS**: distributed file storage, blocks replicated across nodes (fault tolerance).
- **Hive**: lets analysts write SQL that compiles to MapReduce/Tez/Spark jobs under the hood — bridges SQL skills to big data.
- **MapReduce**: original Hadoop processing model (map → shuffle → reduce) — slow due to disk I/O between stages; mostly replaced by Spark today but still referenced in legacy pipelines and interviews.

## Spark (Modern standard for distributed processing)
- In-memory processing → 10-100x faster than MapReduce for iterative jobs.
- Core abstractions: **RDD** (low-level, rarely used directly now) → **DataFrame/Dataset** (optimized via Catalyst + Tungsten).
- See [`spark/spark_batch_job.py`](./spark/spark_batch_job.py) for a full ETL example.
- **Spark Structured Streaming** extends the same DataFrame API to streaming sources (Kafka, files).

## Kafka (Streaming backbone)
- Pub-sub messaging system; topics split into partitions for parallelism.
- See [`kafka/producer_consumer.py`](./kafka/producer_consumer.py) for producer/consumer pattern.
- Key concepts: **offset** (position in partition), **consumer group** (parallel consumers sharing load), **replication factor** (durability).

## Flink
- True stream processing (event-at-a-time, lower latency than Spark micro-batches).
- Strong for complex event processing, exactly-once semantics with stateful functions.

## When to use what
```
Batch processing large historical data     -> Spark (batch mode)
Real-time event processing, low latency    -> Flink or Spark Structured Streaming
SQL access to data stored in HDFS/S3        -> Hive / Presto / Trino
High-throughput event ingestion             -> Kafka
```
