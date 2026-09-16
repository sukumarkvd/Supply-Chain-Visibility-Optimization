SQL ANALYSIS - SUPPLY CHAIN VISIBILITY & OPTIMIZATION

Files:
1. schema.sql              -> creates the MySQL database and tables
2. kpis.sql                -> core project KPIs
3. supplier_analysis.sql   -> supplier performance
4. inventory_analysis.sql  -> inventory and reorder analysis
5. logistics_analysis.sql  -> delivery, warehouse and monthly logistics analysis

Recommended execution order:
1. schema.sql
2. Import the six cleaned CSV files into the matching tables
3. kpis.sql
4. supplier_analysis.sql
5. inventory_analysis.sql
6. logistics_analysis.sql

Database name: supply_chain
