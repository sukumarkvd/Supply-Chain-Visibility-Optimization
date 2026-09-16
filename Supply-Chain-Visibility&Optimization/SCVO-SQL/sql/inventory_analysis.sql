USE supply_chain;

-- Inventory status
SELECT
    i.`Product_ID` AS product_id,
    i.`Warehouse_ID` AS warehouse_id,
    i.`Stock_Units` AS stock_units,
    i.`Reorder_Level` AS reorder_level,
    i.`Safety_Stock` AS safety_stock,
    CASE
        WHEN i.`Stock_Units` <= i.`Safety_Stock` THEN 'Critical - Reorder Immediately'
        WHEN i.`Stock_Units` <= i.`Reorder_Level` THEN 'Reorder Required'
        ELSE 'Healthy'
    END AS inventory_status
FROM inventory i
ORDER BY i.`Stock_Units` ASC;

-- Products with the highest demand
SELECT
    o.`Product_ID` AS product_id,
    p.`Product_Name` AS product_name,
    SUM(o.`Quantity`) AS total_quantity,
    COUNT(DISTINCT o.`Order_ID`) AS total_orders
FROM orders o
LEFT JOIN products p ON o.`Product_ID` = p.`Product_ID`
GROUP BY o.`Product_ID`, p.`Product_Name`
ORDER BY total_quantity DESC
LIMIT 10;

-- Reorder recommendation
SELECT
    i.`Product_ID` AS product_id,
    i.`Warehouse_ID` AS warehouse_id,
    GREATEST(i.`Reorder_Level` + i.`Safety_Stock` - i.`Stock_Units`, 0) AS suggested_reorder_qty
FROM inventory i
WHERE i.`Stock_Units` <= i.`Reorder_Level`
ORDER BY suggested_reorder_qty DESC;
