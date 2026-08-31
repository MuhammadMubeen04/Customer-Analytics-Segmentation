-- ============================================================
-- Customer Analytics & Segmentation - MySQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS customer_analytics;
USE customer_analytics;

-- Customers dimension
CREATE TABLE IF NOT EXISTS customers (
    CustomerID      VARCHAR(20) PRIMARY KEY,
    CustomerName    VARCHAR(100),
    Gender          VARCHAR(10),
    Age             INT,
    AgeGroup        VARCHAR(20),
    City            VARCHAR(50),
    State           VARCHAR(10),
    Region          VARCHAR(20),
    JoinDate        DATE,
    Email           VARCHAR(100)
);

-- Transactions fact table
CREATE TABLE IF NOT EXISTS transactions (
    TransactionID   VARCHAR(20) PRIMARY KEY,
    CustomerID      VARCHAR(20),
    OrderDate       DATE,
    Category        VARCHAR(50),
    Product         VARCHAR(100),
    Quantity        INT,
    UnitPrice       DECIMAL(10,2),
    Discount        DECIMAL(5,2),
    Amount          DECIMAL(12,2),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID)
);

-- ============================================================
-- Import instructions (MySQL Workbench):
-- 1. Right-click table → Table Data Import Wizard
-- 2. Select data/customers.csv → import into customers
-- 3. Select data/transactions.csv → import into transactions
-- ============================================================
