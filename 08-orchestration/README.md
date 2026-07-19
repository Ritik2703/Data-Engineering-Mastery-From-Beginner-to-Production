# 08 — Orchestration

## Tool Comparison
| Tool | Style | Best For |
|---|---|---|
| **Airflow** | DAG (Python), mature, huge ecosystem | Industry standard, complex scheduling, big community/plugins |
| **Prefect** | Python-native, dynamic flows | Simpler local dev experience, dynamic task generation |
| **Dagster** | Asset-based (not just tasks) | Strong data-lineage/testing focus, "software-defined assets" |
| **cron (legacy)** | OS-level scheduler | Simple single scripts, no dependency graph/monitoring/retries |

## Airflow DAG
See full example: [`../04-etl-elt/airflow/etl_dag_example.py`](../04-etl-elt/airflow/etl_dag_example.py)

## Prefect example
```python
from prefect import flow, task

@task(retries=3, retry_delay_seconds=30)
def extract():
    return {"rows": 100}

@task
def transform(data):
    data["rows"] *= 2
    return data

@task
def load(data):
    print(f"Loaded {data['rows']} rows")

@flow(name="orders-pipeline")
def orders_pipeline():
    raw = extract()
    transformed = transform(raw)
    load(transformed)

if __name__ == "__main__":
    orders_pipeline()
```

## Dagster example (asset-based)
```python
from dagster import asset, Definitions

@asset
def raw_orders():
    return {"rows": 100}

@asset
def cleaned_orders(raw_orders):
    raw_orders["rows"] *= 2
    return raw_orders

defs = Definitions(assets=[raw_orders, cleaned_orders])
```

## Choosing an orchestrator
```
Need battle-tested, huge plugin ecosystem, enterprise standard -> Airflow
Need quick Pythonic flows, less boilerplate, dynamic tasks     -> Prefect
Need strong asset lineage + testing built-in                   -> Dagster
Single simple daily script, no dependencies to manage          -> cron (fine for very small scale)
```
