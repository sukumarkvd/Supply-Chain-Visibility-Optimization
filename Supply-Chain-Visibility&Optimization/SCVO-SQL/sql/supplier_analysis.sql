USE supply_chain;

-- Supplier performance: orders, delay and freight cost
SELECT
    o.`None` AS supplier_id,
    s.`Supplier_Name` AS supplier_name,
    COUNT(DISTINCT o.`Order_ID`) AS total_orders,
    ROUND(AVG(sh.`Delay_Days`), 2) AS avg_delay_days,
    ROUND(100.0 * SUM(CASE WHEN sh.`Delay_Days` <= 0 THEN 1 ELSE 0 END) / COUNT(sh.`Order_ID`), 2) AS on_time_delivery_pct,
    ROUND(SUM(sh.`Freight_Cost`), 2) AS total_freight_cost
FROM orders o
LEFT JOIN shipments sh ON o.`Order_ID` = sh.`Order_ID`
LEFT JOIN suppliers s ON o.`None` = s.`None`
GROUP BY o.`None`, s.`Supplier_Name`
ORDER BY on_time_delivery_pct DESC;

-- Suppliers with highest average delay
SELECT
    o.`None` AS supplier_id,
    s.`Supplier_Name` AS supplier_name,
    ROUND(AVG(sh.`Delay_Days`), 2) AS avg_delay_days
FROM orders o
JOIN shipments sh ON o.`Order_ID` = sh.`Order_ID`
LEFT JOIN suppliers s ON o.`None` = s.`None`
GROUP BY o.`None`, s.`Supplier_Name`
ORDER BY avg_delay_days DESC;
