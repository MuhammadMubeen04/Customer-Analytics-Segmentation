# 📊 Customer Analytics & Segmentation (with K-Means)

End-to-end Customer Analytics project that combines **business analytics** with **Machine Learning** (K-Means clustering) to segment customers and drive actionable insights.

**Stack:** SQL → Python (Pandas + Scikit-learn) → Power BI

---

## 📌 Project Overview

This project analyzes customer purchase behavior using RFM (Recency, Frequency, Monetary) metrics and applies **K-Means clustering** to create meaningful customer segments:

- **High-Value Champions**
- **Loyal Frequent**
- **Potential / Occasional**
- **Low-Value / At-Risk**

It demonstrates how a Data Analyst can use Machine Learning in a practical business context (not just a pure ML project).

---

## 🛠️ Tools & Technologies

- **SQL (MySQL)** – Customer & transaction analysis
- **Python** – EDA, RFM engineering, K-Means clustering
- **Pandas & NumPy** – Data manipulation
- **Scikit-learn** – K-Means clustering & evaluation
- **Matplotlib & Seaborn** – Visualizations
- **Power BI** – Interactive segmentation dashboard

---

## ✨ What This Project Covers

### Business Analytics
- Customer demographics (Gender, Age Group, Region)
- Purchase frequency & repeat customers
- Average Order Value (AOV)
- Customer Lifetime Value (proxy via Monetary)
- Recency & churn indicators (Active / Warm / Cool / At-Risk)

### Machine Learning
- RFM feature engineering
- Feature scaling
- K-Means clustering
- Silhouette score for choosing number of clusters
- Business interpretation of clusters → named segments

---

## 📈 Key Insights (from sample data)

- ~9% of customers are **High-Value Champions** but contribute a disproportionately high share of revenue
- A large group of customers show long recency → clear **churn / win-back** opportunity
- Repeat purchase rate is strong, but many customers remain in the low-frequency segment
- Clear behavioral differences exist across the four K-Means segments

---

## 📁 Project Structure

```
customer_analytics_segmentation/
├── data/
│   ├── customers.csv
│   ├── transactions.csv
│   ├── customer_transactions.csv
│   └── summaries/
│       ├── customer_segments.csv      ← main file for Power BI
│       ├── segment_summary.csv
│       └── transactions_with_segment.csv
├── sql/
│   ├── 01_schema_and_load.sql
│   └── 02_analysis_queries.sql
├── python/
│   ├── 01_customer_segmentation.py
│   └── charts/
├── powerbi/
│   └── (place your .pbix here)
├── docs/
│   └── PowerBI_Dashboard_Guide.md
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. SQL (MySQL)
```sql
-- Create database & tables (see sql/01_schema_and_load.sql)
-- Import customers.csv and transactions.csv
-- Run queries in sql/02_analysis_queries.sql
```

### 2. Python
```bash
pip install -r requirements.txt
python python/01_customer_segmentation.py
```
This will:
- Calculate RFM metrics
- Run K-Means clustering
- Generate charts
- Export `customer_segments.csv` for Power BI

### 3. Power BI
- Follow `docs/PowerBI_Dashboard_Guide.md`
- Load `data/summaries/customer_segments.csv`
- Build pages: Overview → Segment Deep Dive → Demographics → Recommendations
- Save as `Customer_Analytics_Segmentation_Dashboard.pbix`

---

## 📊 Recommended Power BI Pages

1. **Executive Overview** – KPIs + Segment distribution + Revenue by Segment  
2. **Segment Deep Dive** – RFM profiles of each segment  
3. **Demographics & Behavior** – Gender, Age, Region by Segment + Recency status  
4. **Actions / Recommendations** – Focus on High-Value retention and At-Risk win-back  

---

## 🎯 Why This Project Stands Out

- Combines classic business metrics with unsupervised Machine Learning
- Shows the full analyst workflow: data → SQL → Python/ML → dashboard
- Produces clear, actionable customer segments that marketing/CRM teams can use
- Perfect complement to a Sales Performance dashboard in a portfolio

---

## 👤 Author

**Your Name**  
Aspiring Data Analyst  

- LinkedIn: [Your LinkedIn]  
- GitHub: [Your GitHub]

---

## 📄 License

Educational & portfolio use.
