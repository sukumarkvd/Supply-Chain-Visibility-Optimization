Supply Chain Visibility & Optimization - Cleaned Dataset
==========================================================

Files:
- products_cleaned.csv
- orders_cleaned.csv
- shipments_cleaned.csv
- inventory_cleaned.csv
- suppliers_cleaned.csv
- warehouses_cleaned.csv
- supply_chain_master_cleaned.csv (order-level analytical dataset)
- cleaning_report.csv

Cleaning performed:
1. Trimmed leading/trailing whitespace from column names and text fields.
2. Converted date fields to standard YYYY-MM-DD format.
3. Converted numeric fields to numeric types.
4. Removed exact duplicate rows.
5. Checked missing values and key relationships.
6. Verified order value = Quantity * Unit_Price.
7. Verified shipment delay days match Actual_Delivery_Date - Expected_Delivery_Date.
8. Created analytical fields in the master file:
   - Order_Lead_Time_Days
   - Shipping_Duration_Days
   - On_Time_Delivery

Quality checks on the supplied data found:
- No missing values.
- No duplicate rows.
- No broken foreign-key relationships among the six source tables.
- No invalid negative quantities/costs/stock values.
- Order values and shipment delay calculations are internally consistent.

Recommended next step:
Use the cleaned source CSVs for SQL/Power BI. Use supply_chain_master_cleaned.csv for order/shipment analysis.
