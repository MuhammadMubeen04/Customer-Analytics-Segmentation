-- ============================================================
-- Customer Analytics & Segmentation - Key SQL Queries (MySQL)
-- ============================================================

USE customer_analytics;

-- ----------------------------------------------------------
-- 1. OVERALL CUSTOMER & REVENUE KPIs
-- ----------------------------------------------------------
SELECT 
    COUNT(DISTINCT c.CustomerID) AS total_customers,
    COUNT(DISTINCT t.TransactionID) AS total_orders,
    ROUND(SUM(t.Amount), 2) AS total_revenue,
    ROUND(AVG(t.Amount), 2) AS avg_order_value,
    ROUND(SUM(t.Amount) / COUNT(DISTINCT c.CustomerID), 2) AS revenue_per_customer
FROM customers c
LEFT JOIN transactions t ON c.CustomerID = t.CustomerID;


-- ----------------------------------------------------------
-- 2. CUSTOMER DEMOGRAPHICS
-- ----------------------------------------------------------
-- By Gender
SELECT 
    Gender,
    COUNT(*) AS customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS pct
FROM customers
GROUP BY Gender;

-- By Age Group
SELECT 
    AgeGroup,
    COUNT(*) AS customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS pct
FROM customers
GROUP BY AgeGroup
ORDER BY AgeGroup;

-- By Region
SELECT 
    Region,
    COUNT(*) AS customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS pct
FROM customers
GROUP BY Region
ORDER BY customers DESC;


-- ----------------------------------------------------------
-- 3. PURCHASE FREQUENCY & REPEAT CUSTOMERS
-- ----------------------------------------------------------
SELECT 
    CASE 
        WHEN order_count = 1 THEN '1 Order (One-time)'
        WHEN order_count BETWEEN 2 AND 3 THEN '2-3 Orders'
        WHEN order_count BETWEEN 4 AND 7 THEN '4-7 Orders'
        ELSE '8+ Orders (Frequent)'
    END AS frequency_band,
    COUNT(*) AS customers,
    ROUND(AVG(total_spent), 2) AS avg_total_spent
FROM (
    SELECT 
        CustomerID,
        COUNT(*) AS order_count,
        SUM(Amount) AS total_spent
    FROM transactions
    GROUP BY CustomerID
) AS cust_orders
GROUP BY 
    CASE 
        WHEN order_count = 1 THEN '1 Order (One-time)'
        WHEN order_count BETWEEN 2 AND 3 THEN '2-3 Orders'
        WHEN order_count BETWEEN 4 AND 7 THEN '4-7 Orders'
        ELSE '8+ Orders (Frequent)'
    END
ORDER BY MIN(order_count);


-- Repeat vs One-time
SELECT 
    CASE WHEN order_count > 1 THEN 'Repeat Customer' ELSE 'One-time Customer' END AS customer_type,
    COUNT(*) AS customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct,
    ROUND(SUM(total_spent), 2) AS total_revenue
FROM (
    SELECT CustomerID, COUNT(*) AS order_count, SUM(Amount) AS total_spent
    FROM transactions
    GROUP BY CustomerID
) t
GROUP BY CASE WHEN order_count > 1 THEN 'Repeat Customer' ELSE 'One-time Customer' END;


-- ----------------------------------------------------------
-- 4. AVERAGE ORDER VALUE & CUSTOMER LIFETIME VALUE (CLV proxy)
-- ----------------------------------------------------------
SELECT 
    CustomerID,
    COUNT(*) AS frequency,
    ROUND(SUM(Amount), 2) AS monetary_value,
    ROUND(AVG(Amount), 2) AS avg_order_value,
    DATEDIFF(MAX(OrderDate), MIN(OrderDate)) AS customer_lifespan_days
FROM transactions
GROUP BY CustomerID
ORDER BY monetary_value DESC
LIMIT 20;


-- ----------------------------------------------------------
-- 5. RECENCY (days since last purchase) - Churn indicator
-- ----------------------------------------------------------
SELECT 
    CASE 
        WHEN days_since_last <= 30 THEN 'Active (0-30 days)'
        WHEN days_since_last <= 90 THEN 'Warm (31-90 days)'
        WHEN days_since_last <= 180 THEN 'Cool (91-180 days)'
        ELSE 'At Risk / Churned (180+ days)'
    END AS recency_status,
    COUNT(*) AS customers
FROM (
    SELECT 
        CustomerID,
        DATEDIFF('2025-06-30', MAX(OrderDate)) AS days_since_last
    FROM transactions
    GROUP BY CustomerID
) r
GROUP BY 
    CASE 
        WHEN days_since_last <= 30 THEN 'Active (0-30 days)'
        WHEN days_since_last <= 90 THEN 'Warm (31-90 days)'
        WHEN days_since_last <= 180 THEN 'Cool (91-180 days)'
        ELSE 'At Risk / Churned (180+ days)'
    END
ORDER BY MIN(days_since_last);


-- ----------------------------------------------------------
-- 6. TOP CUSTOMERS BY REVENUE
-- ----------------------------------------------------------
SELECT 
    c.CustomerID,
    c.CustomerName,
    c.Region,
    c.Gender,
    COUNT(t.TransactionID) AS orders,
    ROUND(SUM(t.Amount), 2) AS total_spent,
    ROUND(AVG(t.Amount), 2) AS avg_order_value
FROM customers c
JOIN transactions t ON c.CustomerID = t.CustomerID
GROUP BY c.CustomerID, c.CustomerName, c.Region, c.Gender
ORDER BY total_spent DESC
LIMIT 15;


-- ----------------------------------------------------------
-- 7. CATEGORY PREFERENCE
-- ----------------------------------------------------------
SELECT 
    Category,
    COUNT(DISTINCT CustomerID) AS unique_customers,
    COUNT(*) AS orders,
    ROUND(SUM(Amount), 2) AS revenue
FROM transactions
GROUP BY Category
ORDER BY revenue DESC;


-- ----------------------------------------------------------
-- 8. MONTHLY TREND
-- ----------------------------------------------------------
SELECT 
    YEAR(OrderDate) AS year,
    MONTH(OrderDate) AS month,
    DATE_FORMAT(OrderDate, '%Y-%m') AS year_month,
    COUNT(DISTINCT CustomerID) AS active_customers,
    COUNT(*) AS orders,
    ROUND(SUM(Amount), 2) AS revenue
FROM transactions
GROUP BY YEAR(OrderDate), MONTH(OrderDate), DATE_FORMAT(OrderDate, '%Y-%m')
ORDER BY year, month;
