"""
Customer Analytics & Segmentation
---------------------------------
1. Exploratory Data Analysis (demographics, frequency, AOV, CLV, churn indicators)
2. RFM Analysis (Recency, Frequency, Monetary)
3. K-Means Clustering to create customer segments
4. Visualizations + export of segmented customer table for Power BI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------
BASE = Path(__file__).parent.parent
DATA = BASE / "data"
CHARTS = Path(__file__).parent / "charts"
CHARTS.mkdir(exist_ok=True)
SUMMARIES = DATA / "summaries"
SUMMARIES.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (11, 6)

# ----------------------------------------------------------
# 1. LOAD DATA
# ----------------------------------------------------------
customers = pd.read_csv(DATA / "customers.csv", parse_dates=["JoinDate"])
transactions = pd.read_csv(DATA / "transactions.csv", parse_dates=["OrderDate"])

print("=" * 60)
print("DATA OVERVIEW")
print("=" * 60)
print(f"Customers: {customers.shape[0]}")
print(f"Transactions: {transactions.shape[0]}")
print(f"Date range: {transactions['OrderDate'].min().date()} → {transactions['OrderDate'].max().date()}")
print(f"Total Revenue: ${transactions['Amount'].sum():,.2f}")

# ----------------------------------------------------------
# 2. BASIC CUSTOMER ANALYTICS
# ----------------------------------------------------------
# Aggregate at customer level
analysis_date = transactions["OrderDate"].max()  # snapshot date

rfm = transactions.groupby("CustomerID").agg(
    Recency=("OrderDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("TransactionID", "count"),
    Monetary=("Amount", "sum"),
    AvgOrderValue=("Amount", "mean"),
    FirstPurchase=("OrderDate", "min"),
    LastPurchase=("OrderDate", "max")
).reset_index()

rfm["AvgOrderValue"] = rfm["AvgOrderValue"].round(2)
rfm["Monetary"] = rfm["Monetary"].round(2)

# Merge demographics
rfm = rfm.merge(customers, on="CustomerID", how="left")

print("\n" + "=" * 60)
print("CUSTOMER LEVEL METRICS (sample)")
print("=" * 60)
print(rfm[["CustomerID", "Recency", "Frequency", "Monetary", "AvgOrderValue", "Gender", "AgeGroup", "Region"]].head(10))

# Overall KPIs
print("\n" + "=" * 60)
print("OVERALL KPIs")
print("=" * 60)
print(f"Total Customers        : {rfm.shape[0]}")
print(f"Total Revenue          : ${rfm['Monetary'].sum():,.2f}")
print(f"Avg Revenue / Customer : ${rfm['Monetary'].mean():,.2f}")
print(f"Avg Frequency          : {rfm['Frequency'].mean():.2f}")
print(f"Avg Order Value        : ${rfm['AvgOrderValue'].mean():,.2f}")
print(f"Avg Recency (days)     : {rfm['Recency'].mean():.1f}")

# Repeat customers
repeat_pct = (rfm["Frequency"] > 1).mean() * 100
print(f"Repeat Customer %      : {repeat_pct:.1f}%")

# ----------------------------------------------------------
# 3. CHURN / RECENCY INDICATORS
# ----------------------------------------------------------
def recency_status(days):
    if days <= 30:
        return "Active (0-30)"
    elif days <= 90:
        return "Warm (31-90)"
    elif days <= 180:
        return "Cool (91-180)"
    else:
        return "At Risk (180+)"

rfm["RecencyStatus"] = rfm["Recency"].apply(recency_status)

print("\n" + "=" * 60)
print("RECENCY / CHURN STATUS")
print("=" * 60)
print(rfm["RecencyStatus"].value_counts())

# ----------------------------------------------------------
# 4. RFM SCORING (optional classic scoring) + K-MEANS
# ----------------------------------------------------------
# Features for clustering
features = ["Recency", "Frequency", "Monetary"]
X = rfm[features].copy()

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find good k using silhouette (try 3 to 6)
print("\n" + "=" * 60)
print("FINDING OPTIMAL K (Silhouette Score)")
print("=" * 60)
sil_scores = {}
for k in range(3, 7):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    sil_scores[k] = score
    print(f"k={k} → Silhouette = {score:.3f}")

best_k = max(sil_scores, key=sil_scores.get)
print(f"\nBest k by silhouette: {best_k}")

# Final model (we use k=4 for clear business segments)
K = 4
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
rfm["Cluster"] = kmeans.fit_predict(X_scaled)

# Interpret clusters by average RFM
cluster_summary = rfm.groupby("Cluster")[features].mean().round(1)
cluster_summary["Count"] = rfm.groupby("Cluster").size()
cluster_summary["Pct"] = (cluster_summary["Count"] / len(rfm) * 100).round(1)
print("\n" + "=" * 60)
print("CLUSTER CENTROIDS (Raw RFM averages)")
print("=" * 60)
print(cluster_summary.sort_values("Monetary", ascending=False))

# Assign business-friendly names based on centroids
# Higher Monetary + Frequency + low Recency = High Value
# We map dynamically
cluster_order = cluster_summary.sort_values("Monetary", ascending=False).index.tolist()

segment_map = {}
names = ["High-Value Champions", "Loyal Frequent", "Potential / Occasional", "Low-Value / At-Risk"]
for i, cl in enumerate(cluster_order):
    segment_map[cl] = names[i] if i < len(names) else f"Segment {cl}"

rfm["Segment"] = rfm["Cluster"].map(segment_map)

print("\n" + "=" * 60)
print("FINAL SEGMENTS")
print("=" * 60)
print(rfm["Segment"].value_counts())

print("\nSegment Profile:")
print(rfm.groupby("Segment")[features + ["AvgOrderValue"]].mean().round(1).sort_values("Monetary", ascending=False))

# ----------------------------------------------------------
# 5. VISUALIZATIONS
# ----------------------------------------------------------
# 5.1 Segment distribution
fig, ax = plt.subplots()
order = rfm["Segment"].value_counts().index
sns.countplot(data=rfm, y="Segment", order=order, ax=ax, palette="viridis")
ax.set_title("Customer Segments (K-Means)")
ax.set_xlabel("Number of Customers")
plt.tight_layout()
plt.savefig(CHARTS / "01_segment_distribution.png", dpi=150)
plt.close()

# 5.2 RFM by Segment (boxplots)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, col in zip(axes, features):
    sns.boxplot(data=rfm, x="Segment", y=col, ax=ax, palette="Set2")
    ax.set_title(col)
    ax.tick_params(axis="x", rotation=30)
plt.suptitle("RFM Distribution by Segment", y=1.02)
plt.tight_layout()
plt.savefig(CHARTS / "02_rfm_by_segment.png", dpi=150)
plt.close()

# 5.3 Monetary vs Frequency scatter colored by Segment
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=rfm, x="Frequency", y="Monetary", hue="Segment", palette="deep", s=60, alpha=0.7, ax=ax)
ax.set_title("Frequency vs Monetary Value by Segment")
plt.tight_layout()
plt.savefig(CHARTS / "03_frequency_vs_monetary.png", dpi=150)
plt.close()

# 5.4 Recency Status
fig, ax = plt.subplots()
sns.countplot(data=rfm, x="RecencyStatus", order=["Active (0-30)", "Warm (31-90)", "Cool (91-180)", "At Risk (180+)"], ax=ax, palette="RdYlGn_r")
ax.set_title("Customer Recency / Churn Status")
ax.tick_params(axis="x", rotation=15)
plt.tight_layout()
plt.savefig(CHARTS / "04_recency_status.png", dpi=150)
plt.close()

# 5.5 Demographics by Segment (Gender)
fig, ax = plt.subplots()
pd.crosstab(rfm["Segment"], rfm["Gender"], normalize="index").plot(kind="bar", stacked=True, ax=ax, colormap="Set2")
ax.set_title("Gender Distribution by Segment")
ax.set_ylabel("Proportion")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig(CHARTS / "05_gender_by_segment.png", dpi=150)
plt.close()

# 5.6 Revenue contribution by Segment
rev_by_seg = rfm.groupby("Segment")["Monetary"].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
rev_by_seg.plot(kind="bar", ax=ax, color="steelblue")
ax.set_title("Total Revenue by Segment")
ax.set_ylabel("Revenue ($)")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig(CHARTS / "06_revenue_by_segment.png", dpi=150)
plt.close()

print(f"\nCharts saved to: {CHARTS}")

# ----------------------------------------------------------
# 6. EXPORT FOR POWER BI & FURTHER USE
# ----------------------------------------------------------
# Full customer profile with segment
rfm_export = rfm[[
    "CustomerID", "CustomerName", "Gender", "Age", "AgeGroup", "City", "State", "Region",
    "JoinDate", "Recency", "Frequency", "Monetary", "AvgOrderValue",
    "FirstPurchase", "LastPurchase", "RecencyStatus", "Cluster", "Segment"
]].copy()

rfm_export.to_csv(SUMMARIES / "customer_segments.csv", index=False)

# Segment summary
seg_summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum"),
    Avg_Order_Value=("AvgOrderValue", "mean")
).round(2).sort_values("Total_Revenue", ascending=False)
seg_summary.to_csv(SUMMARIES / "segment_summary.csv")

# Also save the transactions + segment for richer Power BI model
txn_with_seg = transactions.merge(
    rfm[["CustomerID", "Segment", "RecencyStatus"]], on="CustomerID", how="left"
)
txn_with_seg.to_csv(SUMMARIES / "transactions_with_segment.csv", index=False)

print(f"Summary files exported to: {SUMMARIES}")
print("\n✅ Customer Analytics & K-Means Segmentation complete.")
print("   Next: Load customer_segments.csv (or transactions_with_segment.csv) into Power BI.")
