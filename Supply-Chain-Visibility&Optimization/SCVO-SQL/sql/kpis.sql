USE supply_chain;

-- Core KPIs
SELECT COUNT(DISTINCT `Order_ID`) AS total_orders FROM orders;
SELECT SUM(`Quantity`) AS total_quantity FROM orders;
SELECT SUM(`Order_Value`) AS total_order_value FROM orders;
SELECT AVG(`Order_Value`) AS average_order_value FROM orders;

-- Delivery KPIs
SELECT
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN `Delay_Days` <= 0 THEN 1 ELSE 0 END) AS on_time_shipments,
    ROUND(100.0 * SUM(CASE WHEN `Delay_Days` <= 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS on_time_delivery_pct,
    ROUND(AVG(`Delay_Days`), 2) AS average_delay_days
FROM shipments;

-- Logistics cost
SELECT ROUND(SUM(`Freight_Cost`), 2) AS total_freight_cost FROM shipments;
