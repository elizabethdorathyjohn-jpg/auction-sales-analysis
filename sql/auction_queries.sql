-- =====================================================================
-- Auction Sales Performance and Pricing Analysis — SQL
-- Verified against auction_cleaned_anonymised.csv via SQLite
-- =====================================================================

CREATE TABLE auction_lots (
    public_lot_id               VARCHAR(10) PRIMARY KEY,
    reserve                     DECIMAL(10, 2),
    estimate_minimum            DECIMAL(10, 2),
    estimate_maximum            DECIMAL(10, 2),
    category_descriptions       VARCHAR(100),
    buyers_premium_pct          DECIMAL(5, 2),
    buyers_premium_vat_pct      DECIMAL(5, 2),
    vendors_commission_pct      DECIMAL(5, 2),
    vendors_commission_vat_pct  DECIMAL(5, 2),
    hammer_price                DECIMAL(10, 2),
    hammer_vat_pct              DECIMAL(5, 2),
    sold                        BOOLEAN,
    sale_status                 VARCHAR(20),
    price_performance           VARCHAR(25),
    sold_below_reserve          BOOLEAN,
    buyer_premium_revenue       DECIMAL(10, 2),
    buyer_premium_vat           DECIMAL(10, 2),
    vendor_commission_revenue   DECIMAL(10, 2),
    vendor_commission_vat       DECIMAL(10, 2),
    vendor_id                   VARCHAR(10)
);

-- Q1: Overall sales rate
SELECT
    COUNT(*) AS total_lots,
    SUM(CASE WHEN sale_status = 'Sold' THEN 1 ELSE 0 END) AS sold_lots,
    ROUND(100.0 * SUM(CASE WHEN sale_status = 'Sold' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sales_rate_pct
FROM auction_lots;

-- Q2: Sales rate by category
SELECT
    category_descriptions,
    COUNT(*) AS total_lots,
    SUM(CASE WHEN sale_status = 'Sold' THEN 1 ELSE 0 END) AS sold_lots,
    ROUND(100.0 * SUM(CASE WHEN sale_status = 'Sold' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sales_rate_pct
FROM auction_lots
GROUP BY category_descriptions
ORDER BY sales_rate_pct DESC;

-- Q3: Revenue by category (AVG deliberately excludes unsold zeros: no ELSE clause)
SELECT
    category_descriptions,
    SUM(CASE WHEN sale_status = 'Sold' THEN hammer_price ELSE 0 END) AS total_revenue,
    ROUND(AVG(CASE WHEN sale_status = 'Sold' THEN hammer_price END), 2) AS avg_hammer_price
FROM auction_lots
GROUP BY category_descriptions
ORDER BY total_revenue DESC;

-- Q4: Price performance against estimate (sold lots only)
SELECT
    price_performance,
    COUNT(*) AS lot_count
FROM auction_lots
WHERE sale_status = 'Sold'
GROUP BY price_performance
ORDER BY lot_count DESC;

-- Q5: Vendor performance, anonymised, excluding vendors with <5 lots
SELECT
    vendor_id,
    COUNT(*) AS total_lots,
    SUM(CASE WHEN sale_status = 'Sold' THEN 1 ELSE 0 END) AS sold_lots,
    ROUND(100.0 * SUM(CASE WHEN sale_status = 'Sold' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sales_rate_pct,
    SUM(CASE WHEN sale_status = 'Sold' THEN hammer_price ELSE 0 END) AS total_revenue
FROM auction_lots
GROUP BY vendor_id
HAVING COUNT(*) >= 5
ORDER BY total_revenue DESC;

-- Q6: Lots sold below reserve
SELECT
    COUNT(*) AS sold_lots,
    SUM(CASE WHEN sold_below_reserve = 'True' THEN 1 ELSE 0 END) AS lots_below_reserve,
    ROUND(100.0 * SUM(CASE WHEN sold_below_reserve = 'True' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_below_reserve
FROM auction_lots
WHERE sale_status = 'Sold';

-- Q7: Total buyer premium and vendor commission revenue
SELECT
    ROUND(SUM(buyer_premium_revenue), 2) AS total_buyer_premium_revenue,
    ROUND(SUM(vendor_commission_revenue), 2) AS total_vendor_commission_revenue
FROM auction_lots
WHERE sale_status = 'Sold';

-- Q8: What distinguishes sold lots from unsold lots?
SELECT
    sale_status,
    COUNT(*) AS lot_count,
    ROUND(AVG(estimate_minimum), 2) AS avg_estimate_minimum,
    ROUND(AVG(estimate_maximum), 2) AS avg_estimate_maximum,
    ROUND(AVG(reserve), 2) AS avg_reserve
FROM auction_lots
GROUP BY sale_status;
