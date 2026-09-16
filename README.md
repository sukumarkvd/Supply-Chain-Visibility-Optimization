📦 Supply Chain Visibility & Optimization

📌 Project Overview

Supply Chain Visibility & Optimization is a data analytics and business intelligence project designed to analyze supply chain operations across orders, products, suppliers, shipments, warehouses, and inventory.

The project uses Python, SQL, Excel/CSV, and Power BI to transform raw supply chain data into meaningful business insights and interactive dashboards.

The main objective is to improve visibility into:

- 📊 Sales and order performance
- 📦 Product demand
- 🚚 Shipment and delivery performance
- 🏭 Supplier performance
- 🏢 Warehouse operations
- 💰 Freight and logistics costs
- 📋 Inventory levels
- 🔄 Reorder requirements
- 📈 Demand and inventory optimization

---

🎯 Project Objectives

The key objectives of this project are:

1. Analyze overall supply chain performance.
2. Identify sales and demand trends.
3. Analyze supplier and logistics performance.
4. Monitor warehouse delivery performance.
5. Identify inventory shortages and reorder requirements.
6. Analyze freight and transportation costs.
7. Build an interactive Power BI dashboard.
8. Generate data-driven insights for supply chain optimization.

---

🛠️ Technologies Used

Technology| Purpose
Python| Data cleaning, EDA, analysis and optimization
Pandas| Data manipulation and transformation
NumPy| Numerical analysis and calculations
Matplotlib| Data visualization
SQL| Database analysis and KPI queries
Power BI| Interactive dashboards and business intelligence
DAX| Power BI measures and calculations
Excel/CSV| Data storage and preprocessing
GitHub| Project version control and documentation

---

📂 Dataset

The project uses six main datasets:

products.csv
orders.csv
shipments.csv
inventory.csv
suppliers.csv
warehouses.csv

Dataset Description

Products

Contains information about products and their categories.

Important fields:

Product_ID
Product_Name
Category

Orders

Contains customer order and sales information.

Important fields:

Order_ID
Product_ID
Supplier_ID
Warehouse_ID
Order_Date
Quantity
Unit_Price
Order_Value

Shipments

Contains shipment and delivery information.

Important fields:

Shipment_ID
Order_ID
Supplier_ID
Warehouse_ID
Shipment_Date
Expected_Delivery_Date
Actual_Delivery_Date
Delay_Days
Freight_Cost
Shipping_Mode

Inventory

Contains inventory and stock information.

Important fields:

Inventory_ID
Product_ID
Warehouse_ID
Stock_Units
Reorder_Level
Safety_Stock
Inventory_Date
Stock_Value

Suppliers

Contains supplier information.

Warehouses

Contains warehouse information.

---

🔄 Project Workflow

Raw Dataset
     ↓
Data Cleaning
     ↓
Data Validation
     ↓
Exploratory Data Analysis
     ↓
Python Analysis
     ↓
SQL Analysis
     ↓
Power BI Data Model
     ↓
DAX Calculations
     ↓
Interactive Dashboard
     ↓
Business Insights
     ↓
Supply Chain Optimization

---

🐍 Python Analysis

Python was used to clean, transform and analyze the supply chain data.

Main Python tasks

- Load CSV datasets
- Clean column names
- Standardize data types
- Handle date fields
- Check missing values
- Check duplicate records
- Validate relationships
- Calculate supply chain KPIs
- Analyze product demand
- Analyze supplier performance
- Analyze warehouse performance
- Analyze monthly trends
- Generate visualizations
- Identify inventory optimization opportunities

Python Libraries

pandas
numpy
matplotlib

Install them using:

pip install pandas numpy matplotlib

Run the project:

python supply_chain_project.py

---

🗄️ SQL Analysis

SQL was used to perform structured analysis of the supply chain database.

The SQL section contains:

sql/
├── schema.sql
├── kpis.sql
├── supplier_analysis.sql
├── inventory_analysis.sql
└── logistics_analysis.sql

SQL Analysis Includes

- Total orders
- Total sales
- Total quantity
- Supplier performance
- Freight cost analysis
- Inventory analysis
- Reorder analysis
- Shipment performance
- Delivery delay analysis
- Warehouse analysis

---

📊 Power BI Dashboard

The project contains a four-page Power BI dashboard.

Page 1 — Executive Overview

The first page provides a high-level overview of the complete supply chain.

KPIs

- Total Orders
- Total Sales
- Total Quantity
- Total Freight Cost
- On-Time Delivery %

Visualizations

- Monthly Sales Trend
- Top 10 Products by Sales
- Delivery Performance
- Executive Insights

Filters

- Order Date
- Supplier
- Warehouse
- Category

---

📈 Page 2 — Sales & Demand Analysis

The second page focuses on product sales and demand trends.

KPIs

- Total Sales
- Total Quantity
- Average Order Value
- Average Quantity per Order

Visualizations

- Monthly Demand Trend
- Top 10 Products by Sales
- Sales by Category
- Product-wise Demand

Filters

- Order Date
- Product
- Category

The actual dashboard shows approximately:

- Total Sales: ₹2.37B
- Total Quantity: 1.82M units
- Average Order Value: ₹197,230
- Average Quantity per Order: 151.7 units

---

🚚 Page 3 — Supplier & Logistics Analysis

The third page analyzes suppliers, shipments, warehouses and logistics costs.

KPIs

- Total Shipments
- Freight Cost
- On-Time Delivery
- Average Delay

Visualizations

- Top 10 Suppliers by Freight Cost
- Warehouse On-Time Delivery Performance
- Average Shipment Delay Trend
- Monthly Freight Cost Trend

Filters

- Shipment Date
- Supplier
- Warehouse
- Shipping Mode

Actual dashboard values include:

- Total Shipments: 12,000
- Freight Cost: ₹5.05M
- On-Time Delivery: 33.58%
- Average Delay: 3.08 days

---

📦 Page 4 — Inventory & Optimization Analysis

The fourth page focuses on inventory management and optimization.

KPIs

- Total Inventory Units
- Products Tracked
- Reorder Alerts
- Total Inventory Value

Visualizations

- Top 10 Products by Inventory Stock
- Lowest Stock Coverage Products
- Inventory by Warehouse
- Inventory Reorder Status

Optimization Metrics

- Stock Coverage
- Inventory Gap
- Reorder Status
- Demand-based replenishment

Actual dashboard values include:

- Total Inventory Units: 4,544,622
- Products Tracked: 200
- Reorder Alerts: 309
- Average Stock/Demand: 0.28×

The inventory reorder analysis shows 82.8% sufficient stock and 17.2% requiring reorder in the dashboard data.

---

🧮 Important DAX Measures

Total Sales

Total Sales =
SUM(orders_cleaned[Order_Value])

Total Quantity

Total Quantity =
SUM(orders_cleaned[Quantity])

Total Orders

Total Orders =
DISTINCTCOUNT(orders_cleaned[Order_ID])

Average Order Value

Average Order Value =
DIVIDE(
    [Total Sales],
    [Total Orders]
)

On-Time Delivery %

On-Time Delivery % =
DIVIDE(
    CALCULATE(
        COUNTROWS(shipments_cleaned),
        shipments_cleaned[Delay_Days] <= 0
    ),
    COUNTROWS(shipments_cleaned)
)

Average Delay

Average Delay =
AVERAGE(shipments_cleaned[Delay_Days])

Total Freight Cost

Total Freight Cost =
SUM(shipments_cleaned[Freight_Cost])

Total Inventory Units

Total Inventory Units =
SUM(inventory_cleaned[Stock_Units])

Reorder Alerts

Reorder Alerts =
CALCULATE(
    COUNTROWS(inventory_cleaned),
    inventory_cleaned[Stock_Units]
        <= inventory_cleaned[Reorder_Level]
)

Stock Coverage

Stock Coverage =
DIVIDE(
    [Total Inventory Units],
    [Total Demand]
)

Reorder Status

Reorder Status =
IF(
    inventory_cleaned[Stock_Units]
        <= inventory_cleaned[Reorder_Level],
    "Reorder Required",
    "Sufficient Stock"
)

---

📁 Project Structure

Supply-Chain-Visibility-Optimization/
│
├── data/
│   ├── products_cleaned.csv
│   ├── orders_cleaned.csv
│   ├── shipments_cleaned.csv
│   ├── inventory_cleaned.csv
│   ├── suppliers_cleaned.csv
│   └── warehouses_cleaned.csv
│
├── python/
│   ├── etl.py
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── forecasting.py
│   └── optimization.py
│
├── sql/
│   ├── schema.sql
│   ├── kpis.sql
│   ├── supplier_analysis.sql
│   ├── inventory_analysis.sql
│   └── logistics_analysis.sql
│
├── powerbi/
│   ├── Page1_Executive_Overview
│   ├── Page2_Sales_Demand_Analysis
│   ├── Page3_Supplier_Logistics_Analysis
│   ├── Page4_Inventory_Optimization_Analysis
│   ├── DAX_Measures.txt
│   └── SupplyChain_Theme.json
│
├── reports/
│   ├── cleaning_report.csv
│   └── project_report.pdf
│
├── README.md
└── requirements.txt

---

🔗 Data Model

The main relationships used in the Power BI model are:

Products
   │
   └── Product_ID
          │
          ↓
       Orders
       │    │
       │    ├──────── Supplier_ID → Suppliers
       │    │
       │    └──────── Warehouse_ID → Warehouses
       │
       └── Order_ID
              │
              ↓
          Shipments

Inventory is connected through:

Products → Product_ID → Inventory
Warehouses → Warehouse_ID → Inventory

---

📌 Key Findings

The analysis produced several important observations:

- The dataset contains 12,000 orders/shipments.
- Total sales are approximately ₹2.37B.
- Total ordered quantity is approximately 1.82M units.
- Total freight cost is approximately ₹5.05M.
- On-time delivery is approximately 33.58%.
- Average shipment delay is approximately 3.08 days.
- Inventory contains approximately 4.54M units.
- 200 products are tracked in inventory.
- 309 inventory records are identified as reorder alerts.
- Inventory and demand analysis can be used to support replenishment planning.

---

💡 Business Optimization Areas

Based on the dashboard analysis, the project focuses on several optimization areas:

🚚 Logistics

Monitor delivery delays and freight costs to identify areas for logistics improvement.

🏭 Supplier Management

Analyze supplier freight costs and shipment performance.

🏢 Warehouse Management

Compare warehouse inventory distribution and delivery performance.

📦 Inventory Management

Monitor stock levels against reorder levels and safety stock.

📈 Demand Planning

Analyze product demand trends to support inventory replenishment decisions.

---

🚀 Future Enhancements

Possible future improvements include:

- Machine-learning-based demand forecasting
- Customer churn analysis
- Advanced inventory optimization
- Automated reorder recommendations
- Supplier risk scoring
- Route optimization
- Real-time supply chain monitoring
- Automated Power BI refresh
- Predictive delivery-delay modeling
- Integration with live ERP or logistics systems

---

🎓 Project Type

Academic / B.Tech Data Analytics & Business Intelligence Project

Skills Demonstrated

- Python
- SQL
- Power BI
- DAX
- Data Cleaning
- Exploratory Data Analysis
- Data Visualization
- Business Intelligence
- Supply Chain Analytics
- Inventory Analytics
- Logistics Analytics
- Data-driven Decision Making



⭐ Project Summary

Supply Chain Visibility & Optimization demonstrates how raw operational data can be transformed into actionable business intelligence using Python, SQL, and Power BI.

The project provides visibility across sales, demand, suppliers, logistics, warehouses, and inventory, with interactive dashboards designed to support supply chain monitoring and optimization.You can save the above directly as README.md in your GitHub repository.
