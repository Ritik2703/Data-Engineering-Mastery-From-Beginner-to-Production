# 10 — DevOps for Data Engineers

## Why DE needs DevOps skills
Pipelines are software — they need version control, testing, containerization, and automated deployment just like application code.

## Docker
- Package pipeline code + dependencies into a reproducible image — "works on my machine" problem solved.
- See [`docker/Dockerfile`](./docker/Dockerfile) for a Python ETL container example.
- Common pattern: Airflow workers run tasks inside Docker containers (`DockerOperator`) or Kubernetes pods (`KubernetesPodOperator`) for isolation.

## Kubernetes (K8s) — DE-relevant concepts
- **KubernetesExecutor** in Airflow — spins up a new pod per task, auto-scales, cleans up after completion.
- **CronJob** — K8s-native way to schedule containerized batch jobs (alternative to Airflow for very simple cases).
- **Helm charts** — package/deploy Airflow, Spark, or Kafka on K8s with configurable values.

## CI/CD
See [`ci-cd/github-actions-pipeline.yml`](./ci-cd/github-actions-pipeline.yml): lint → unit test → dbt test → build Docker image → push → deploy DAGs.

Key principle: **test data pipelines like code**
- Unit test transformation logic (pure functions, mock data)
- `dbt test` for data quality assertions
- Integration test against a sample/staging dataset before production deploy

## Git Best Practices for DE repos
- Feature branches per pipeline change, PR review before merging to `main`
- Never commit credentials — use `.env` (gitignored) + Secrets Manager/Key Vault in production
- Tag releases when deploying major schema/logic changes (helps rollback)
- `.gitignore` should include: `__pycache__/`, `*.pyc`, `.env`, `target/` (dbt), `logs/`
