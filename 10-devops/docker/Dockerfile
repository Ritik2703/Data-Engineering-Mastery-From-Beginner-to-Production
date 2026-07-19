# Dockerfile for a Python ETL pipeline (e.g., Airflow task or standalone script container)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user for security best practice
RUN useradd -m etluser
USER etluser

ENTRYPOINT ["python", "rest_api_to_postgres.py"]
