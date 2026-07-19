"""
Scenario: Pull paginated data from a REST API and load it into PostgreSQL.
Covers: pagination, retries/backoff, incremental load (watermark), bulk insert.

pip install requests psycopg2-binary tenacity python-dotenv
"""

import os
import requests
import psycopg2
from psycopg2.extras import execute_values
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime

API_BASE_URL = "https://api.example.com/v1/orders"
API_KEY = os.getenv("API_KEY")
PG_CONN = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
    "dbname": os.getenv("PG_DB", "warehouse"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD"),
}


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30))
def fetch_page(cursor: str | None, updated_since: str) -> dict:
    """Fetch one page of data from the API with retry/backoff on failure."""
    params = {"updated_since": updated_since, "limit": 500}
    if cursor:
        params["cursor"] = cursor
    resp = requests.get(
        API_BASE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_last_watermark(conn) -> str:
    """Incremental load pattern: read last successful load timestamp."""
    with conn.cursor() as cur:
        cur.execute("SELECT MAX(updated_at) FROM raw_orders;")
        row = cur.fetchone()
        return row[0].isoformat() if row and row[0] else "2020-01-01T00:00:00Z"


def load_batch(conn, rows: list[dict]):
    """Bulk insert using execute_values (much faster than row-by-row inserts)."""
    if not rows:
        return
    query = """
        INSERT INTO raw_orders (order_id, customer_id, amount, status, updated_at)
        VALUES %s
        ON CONFLICT (order_id) DO UPDATE
        SET amount = EXCLUDED.amount,
            status = EXCLUDED.status,
            updated_at = EXCLUDED.updated_at;
    """
    values = [
        (r["id"], r["customer_id"], r["amount"], r["status"], r["updated_at"])
        for r in rows
    ]
    with conn.cursor() as cur:
        execute_values(cur, query, values, page_size=500)
    conn.commit()


def main():
    conn = psycopg2.connect(**PG_CONN)
    try:
        watermark = get_last_watermark(conn)
        cursor = None
        total_loaded = 0

        while True:
            page = fetch_page(cursor, watermark)
            rows = page.get("data", [])
            load_batch(conn, rows)
            total_loaded += len(rows)

            cursor = page.get("next_cursor")
            if not cursor:
                break

        print(f"[{datetime.utcnow()}] Loaded {total_loaded} rows since {watermark}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
