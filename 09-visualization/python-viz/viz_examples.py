"""
Python visualization quick reference for DE reporting/validation (not a replacement for BI tools,
but useful for pipeline QA, notebooks, and ad-hoc analysis).
pip install matplotlib seaborn plotly pandas
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_csv("monthly_sales.csv")  # columns: month, region, total_sales

# ---------------- Matplotlib: quick line chart ----------------
plt.figure(figsize=(10, 5))
for region in df["region"].unique():
    subset = df[df["region"] == region]
    plt.plot(subset["month"], subset["total_sales"], marker="o", label=region)
plt.title("Monthly Sales by Region")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_sales_trend.png")

# ---------------- Seaborn: heatmap for correlation / pivoted data ----------------
pivot = df.pivot_table(index="region", columns="month", values="total_sales", aggfunc="sum")
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues")
plt.title("Sales Heatmap: Region x Month")
plt.savefig("sales_heatmap.png")

# ---------------- Plotly: interactive dashboard-style chart (great for notebooks) ----------------
fig = px.bar(
    df, x="month", y="total_sales", color="region",
    barmode="group", title="Monthly Sales by Region (Interactive)"
)
fig.write_html("interactive_sales_chart.html")
# fig.show()  # opens in browser/notebook
