# 09 — Visualization

## Tableau — Core Concepts
- **Extract vs Live connection**: Extract = snapshot (.hyper file, faster, needs refresh schedule); Live = always current, hits source DB every query.
- **Dimensions vs Measures**: Dimensions = qualitative/categorical (region, product); Measures = quantitative/aggregatable (sales, quantity).
- **Calculated Fields**: e.g. `IF [Sales] > 1000 THEN "High" ELSE "Low" END`
- **LOD (Level of Detail) Expressions**: `{FIXED [Region] : SUM([Sales])}` — compute aggregation at a different granularity than the view.
- **Blending vs Joining**: Joining = combine at data-source level (same source or compatible); Blending = combine dashboards from different data sources at aggregate level.
- Publish to **Tableau Server/Cloud** with scheduled extract refreshes tied to the underlying ETL pipeline's completion.

## Power BI — Core Concepts
- **Power Query (M language)**: the ETL/transform layer inside Power BI — similar to dbt but GUI-driven, runs before data loads into the model.
- **DAX (Data Analysis Expressions)**: formula language for measures.
  ```
  Total Sales = SUM(Orders[Amount])
  YoY Growth % = 
      DIVIDE(
          [Total Sales] - CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date])),
          CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
      )
  ```
- **Star Schema modeling** in Power BI's model view — same dimensional modeling concepts from `01-fundamentals/` apply directly.
- **Import vs DirectQuery mode**: Import = data cached in-memory (fast, needs refresh); DirectQuery = live query to source (always fresh, slower, source load).
- **Row-Level Security (RLS)**: restrict which rows a user sees based on their identity — critical for enterprise dashboards.
- Publish to **Power BI Service**, schedule refresh tied to pipeline completion (or use Power BI's REST API to trigger refresh programmatically after ETL finishes).

## Trigger refresh via Power BI REST API (common DE integration point)
```python
import requests

url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
headers = {"Authorization": f"Bearer {access_token}"}
requests.post(url, headers=headers)
```

## Python Visualization (for pipeline QA / notebooks, not BI replacement)
See [`python-viz/viz_examples.py`](./python-viz/viz_examples.py) — matplotlib, seaborn heatmaps, plotly interactive charts.

## Choosing a BI tool
```
Microsoft-stack org, need deep Excel/Azure integration -> Power BI
Need highly polished, flexible/free-form visual design -> Tableau
Need embedded analytics inside a custom app             -> Looker / Power BI Embedded / Superset (OSS)
```
