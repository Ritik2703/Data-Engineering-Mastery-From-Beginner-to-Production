"""
Database connection cheat sheet — every major DB, one pattern each.
pip install psycopg2-binary pymysql pymongo snowflake-connector-python sqlalchemy cx_Oracle
"""

# ---------- PostgreSQL ----------
import psycopg2
pg_conn = psycopg2.connect(
    host="localhost", port=5432, dbname="mydb", user="postgres", password="secret"
)

# ---------- MySQL ----------
import pymysql
mysql_conn = pymysql.connect(
    host="localhost", port=3306, db="mydb", user="root", password="secret"
)

# ---------- MongoDB (NoSQL) ----------
from pymongo import MongoClient
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["mydb"]
docs = list(mongo_db["orders"].find({"status": "completed"}).limit(100))

# ---------- Snowflake ----------
import snowflake.connector
sf_conn = snowflake.connector.connect(
    user="my_user",
    password="secret",
    account="xy12345.ap-south-1",
    warehouse="COMPUTE_WH",
    database="ANALYTICS",
    schema="PUBLIC",
)
cur = sf_conn.cursor()
cur.execute("SELECT * FROM fact_sales LIMIT 10;")
rows = cur.fetchall()

# ---------- SQLAlchemy (universal ORM/engine — recommended for pandas) ----------
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql+psycopg2://postgres:secret@localhost:5432/mydb")
df = pd.read_sql("SELECT * FROM orders WHERE order_date >= '2026-01-01'", engine)

# Write back (common ETL load step)
df.to_sql("orders_summary", engine, if_exists="replace", index=False, chunksize=1000)

# ---------- Oracle (legacy but very common in enterprises) ----------
import cx_Oracle
oracle_conn = cx_Oracle.connect(
    user="system", password="secret", dsn="localhost:1521/orclpdb"
)

# ---------- Redshift (uses postgres protocol) ----------
redshift_conn = psycopg2.connect(
    host="my-cluster.xxxx.ap-south-1.redshift.amazonaws.com",
    port=5439, dbname="dev", user="awsuser", password="secret"
)

# ---------- SQL Server (legacy enterprise, via pyodbc) ----------
import pyodbc
mssql_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;DATABASE=mydb;UID=sa;PWD=secret"
)
