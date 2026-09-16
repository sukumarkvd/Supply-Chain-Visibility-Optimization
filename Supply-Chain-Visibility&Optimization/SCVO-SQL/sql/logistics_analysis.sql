USE supply_chain;

-- Delivery status summary
SELECT
    CASE WHEN `Delay_Days` <= 0 THEN 'On Time' ELSE 'Delayed' END AS delivery_status,
    COUNT(*) AS shipment_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM shipments), 2) AS percentage
FROM shipments
GROUP BY delivery_status;

-- Average delay and freight cost by warehouse
SELECT
    o.`Warehouse_ID` AS warehouse_id,
    w.`Warehouse_Name` AS warehouse_name,
    COUNT(DISTINCT o.`Order_ID`) AS orders,
    ROUND(AVG(sh.`Delay_Days`), 2) AS avg_delay_days,
    ROUND(SUM(sh.`Freight_Cost`), 2) AS total_freight_cost
FROM orders o
JOIN shipments sh ON o.`Order_ID` = sh.`Order_ID`
LEFT JOIN warehouses w ON o.`Warehouse_ID` = w.`Warehouse_ID`
GROUP BY o.`Warehouse_ID`, w.`Warehouse_Name`
ORDER BY avg_delay_days DESC;

-- Monthly order performance
SELECT
    DATE_FORMAT(`Order_Date`, '%Y-%m') AS order_month,
    COUNT(DISTINCT `Order_ID`) AS orders,
    SUM(`Quantity`) AS quantity,
    ROUND(SUM(`Order_Value`), 2) AS order_value
FROM orders
GROUP BY DATE_FORMAT(`Order_Date`, '%Y-%m')
ORDER BY order_month;
