"""
Supply Chain Visibility & Optimization
Integrated Python pipeline:
ETL -> Data Cleaning -> EDA -> Demand Forecasting -> Optimization

Expected input files inside the data/ folder:
- orders_cleaned.csv
- shipments_cleaned.csv
- products_cleaned.csv
- suppliers_cleaned.csv
- warehouses_cleaned.csv
- inventory_cleaned.csv
- supply_chain_master_cleaned.csv (optional; created by this script if absent)

Run:
    python supply_chain_project.py

Outputs are written to the outputs/ folder.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. PROJECT PATHS
# -----------------------------
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

FILES = {
    "orders": DATA_DIR / "orders_cleaned.csv",
    "shipments": DATA_DIR / "shipments_cleaned.csv",
    "products": DATA_DIR / "products_cleaned.csv",
    "suppliers": DATA_DIR / "suppliers_cleaned.csv",
    "warehouses": DATA_DIR / "warehouses_cleaned.csv",
    "inventory": DATA_DIR / "inventory_cleaned.csv",
}


# -----------------------------
# 2. ETL
# -----------------------------
def load_data():
    """Extract CSV files and load them into Pandas DataFrames."""
    data = {}
    for name, path in FILES.items():
        if not path.exists():
            raise FileNotFoundError(
                f"Missing file: {path}\n"
                "Put all cleaned CSV files inside the project's data/ folder."
            )
        data[name] = pd.read_csv(path)

    print("\n=== ETL: DATA LOADED ===")
    for name, df in data.items():
        print(f"{name:12s}: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return data


def prepare_dates(data):
    """Convert date columns to datetime."""
    date_columns = {
        "orders": ["Order_Date"],
        "shipments": ["Shipping_Date", "Expected_Delivery_Date", "Actual_Delivery_Date"],
        "inventory": ["Inventory_Date"],
    }

    for table, columns in date_columns.items():
        for col in columns:
            if col in data[table].columns:
                data[table][col] = pd.to_datetime(
                    data[table][col], errors="coerce"
                )
    return data


def build_master(data):
    """Create a single analytical table by joining the cleaned tables."""
    orders = data["orders"].copy()
    shipments = data["shipments"].copy()
    products = data["products"].copy()
    suppliers = data["suppliers"].copy()
    warehouses = data["warehouses"].copy()

    master = orders.merge(
        shipments,
        on="Order_ID",
        how="left",
        suffixes=("", "_shipment")
    )

    master = master.merge(
        products,
        on="Product_ID",
        how="left",
        suffixes=("", "_product")
    )

    # Supplier_ID already exists in shipments, so use it for supplier join.
    master = master.merge(
        suppliers,
        on="Supplier_ID",
        how="left",
        suffixes=("", "_supplier")
    )

    master = master.merge(
        warehouses,
        on="Warehouse_ID",
        how="left",
        suffixes=("", "_warehouse")
    )

    # Derived operational metrics.
    if {"Actual_Delivery_Date", "Order_Date"}.issubset(master.columns):
        master["Order_Lead_Time_Days"] = (
            master["Actual_Delivery_Date"] - master["Order_Date"]
        ).dt.days

    if {"Actual_Delivery_Date", "Shipping_Date"}.issubset(master.columns):
        master["Shipping_Duration_Days"] = (
            master["Actual_Delivery_Date"] - master["Shipping_Date"]
        ).dt.days

    if "Delay_Days" in master.columns:
        master["On_Time_Delivery"] = np.where(
            master["Delay_Days"].fillna(0) <= 0, "On Time", "Delayed"
        )

    return master


# -----------------------------
# 3. DATA CLEANING
# -----------------------------
def clean_data(data):
    """Perform general, safe cleaning on all tables."""
    print("\n=== DATA CLEANING ===")

    for name, df in data.items():
        before = len(df)

        # Remove exact duplicate rows.
        data[name] = df.drop_duplicates().copy()

        # Clean column names.
        data[name].columns = (
            data[name].columns
            .str.strip()
            .str.replace(" ", "_", regex=False)
        )

        # Strip whitespace from text columns.
        for col in data[name].select_dtypes(include="object").columns:
            data[name][col] = data[name][col].apply(
                lambda x: x.strip() if isinstance(x, str) else x
            )

        removed = before - len(data[name])
        print(f"{name:12s}: {removed} duplicate rows removed")

    return data


# -----------------------------
# 4. EDA
# -----------------------------
def run_eda(data, master):
    """Create key descriptive analyses and charts."""
    print("\n=== EDA ===")

    # KPI summary.
    kpis = {
        "Total Orders": len(data["orders"]),
        "Total Quantity": data["orders"]["Quantity"].sum(),
        "Total Order Value": data["orders"]["Order_Value"].sum(),
        "Average Order Value": data["orders"]["Order_Value"].mean(),
        "Average Lead Time (Days)": master["Order_Lead_Time_Days"].mean(),
        "On-Time Delivery %": (
            master["On_Time_Delivery"].eq("On Time").mean() * 100
        ),
        "Total Freight Cost": master["Freight_Cost"].sum(),
    }
    kpi_df = pd.DataFrame(
        {"Metric": list(kpis.keys()), "Value": list(kpis.values())}
    )
    kpi_df.to_csv(OUTPUT_DIR / "kpi_summary.csv", index=False)

    # Product demand.
    product_demand = (
        master.groupby(["Product_ID", "Product_Name"], as_index=False)
        .agg(
            Total_Quantity=("Quantity", "sum"),
            Total_Order_Value=("Order_Value", "sum"),
            Number_of_Orders=("Order_ID", "nunique"),
        )
        .sort_values("Total_Quantity", ascending=False)
    )
    product_demand.to_csv(OUTPUT_DIR / "product_demand.csv", index=False)

    # Supplier performance.
    supplier_perf = (
        master.groupby(["Supplier_ID", "Supplier_Name"], as_index=False)
        .agg(
            Orders=("Order_ID", "nunique"),
            Average_Delay_Days=("Delay_Days", "mean"),
            On_Time_Delivery_Pct=(
                "On_Time_Delivery",
                lambda x: (x.eq("On Time").mean() * 100),
            ),
            Average_Lead_Time_Days=("Order_Lead_Time_Days", "mean"),
            Freight_Cost=("Freight_Cost", "sum"),
        )
        .sort_values("On_Time_Delivery_Pct", ascending=False)
    )
    supplier_perf.to_csv(OUTPUT_DIR / "supplier_performance.csv", index=False)

    # Warehouse performance.
    warehouse_perf = (
        master.groupby(
            ["Warehouse_ID", "Warehouse_Name"], as_index=False
        )
        .agg(
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
            Order_Value=("Order_Value", "sum"),
            Average_Lead_Time_Days=("Order_Lead_Time_Days", "mean"),
        )
        .sort_values("Orders", ascending=False)
    )
    warehouse_perf.to_csv(OUTPUT_DIR / "warehouse_performance.csv", index=False)

    # Monthly order trend.
    orders = data["orders"].copy()
    orders["Month"] = orders["Order_Date"].dt.to_period("M").astype(str)
    monthly = (
        orders.groupby("Month", as_index=False)
        .agg(
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
            Order_Value=("Order_Value", "sum"),
        )
    )
    monthly.to_csv(OUTPUT_DIR / "monthly_demand.csv", index=False)

    # Plot 1: monthly demand.
    plt.figure(figsize=(10, 5))
    plt.plot(monthly["Month"], monthly["Quantity"], marker="o")
    plt.title("Monthly Supply Chain Demand")
    plt.xlabel("Month")
    plt.ylabel("Quantity")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_demand.png", dpi=150)
    plt.close()

    # Plot 2: top 10 products.
    top10 = product_demand.head(10).sort_values("Total_Quantity")
    plt.figure(figsize=(10, 6))
    plt.barh(top10["Product_Name"].astype(str), top10["Total_Quantity"])
    plt.title("Top 10 Products by Demand")
    plt.xlabel("Quantity")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_10_products.png", dpi=150)
    plt.close()

    # Plot 3: supplier on-time performance.
    top_suppliers = supplier_perf.sort_values(
        "On_Time_Delivery_Pct", ascending=False
    ).head(10)
    plt.figure(figsize=(10, 6))
    plt.bar(
        top_suppliers["Supplier_Name"].astype(str),
        top_suppliers["On_Time_Delivery_Pct"],
    )
    plt.title("Top Suppliers by On-Time Delivery")
    plt.xlabel("Supplier")
    plt.ylabel("On-Time Delivery %")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "supplier_on_time.png", dpi=150)
    plt.close()

    print("EDA outputs saved to:", OUTPUT_DIR)


# -----------------------------
# 5. FORECASTING
# -----------------------------
def forecast_demand(data, periods=3):
    """
    Simple baseline demand forecast using a linear trend.
    This is intentionally lightweight so it runs without extra ML packages.
    """
    print("\n=== DEMAND FORECASTING ===")

    orders = data["orders"].copy()
    orders["Month"] = orders["Order_Date"].dt.to_period("M")

    monthly = (
        orders.groupby("Month", as_index=False)["Quantity"]
        .sum()
        .sort_values("Month")
    )

    if len(monthly) < 3:
        print("Not enough monthly history for a trend forecast.")
        return

    y = monthly["Quantity"].astype(float).to_numpy()
    x = np.arange(len(y), dtype=float)

    # Linear regression with NumPy.
    slope, intercept = np.polyfit(x, y, 1)

    future_x = np.arange(len(y), len(y) + periods, dtype=float)
    forecast_values = np.maximum(
        0, intercept + slope * future_x
    )

    last_month = monthly["Month"].iloc[-1]
    future_months = [
        last_month + i for i in range(1, periods + 1)
    ]

    forecast_df = pd.DataFrame(
        {
            "Forecast_Month": [str(m) for m in future_months],
            "Forecast_Quantity": np.round(forecast_values, 0).astype(int),
        }
    )
    forecast_df.to_csv(OUTPUT_DIR / "demand_forecast.csv", index=False)

    # Plot actual + forecast.
    plt.figure(figsize=(10, 5))
    plt.plot(
        [str(m) for m in monthly["Month"]],
        monthly["Quantity"],
        marker="o",
        label="Actual",
    )
    plt.plot(
        forecast_df["Forecast_Month"],
        forecast_df["Forecast_Quantity"],
        marker="o",
        linestyle="--",
        label="Forecast",
    )
    plt.title("Supply Chain Demand Forecast")
    plt.xlabel("Month")
    plt.ylabel("Quantity")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "demand_forecast.png", dpi=150)
    plt.close()

    print(forecast_df.to_string(index=False))


# -----------------------------
# 6. OPTIMIZATION
# -----------------------------
def optimize_inventory(data):
    """
    Create practical inventory recommendations:
    - Reorder if stock is at/below reorder level.
    - Suggested order quantity = safety stock gap.
    """
    print("\n=== INVENTORY OPTIMIZATION ===")

    inv = data["inventory"].copy()

    required = {
        "Product_ID",
        "Warehouse_ID",
        "Stock_Units",
        "Reorder_Level",
        "Safety_Stock",
    }
    missing = required - set(inv.columns)
    if missing:
        print("Inventory optimization skipped. Missing:", sorted(missing))
        return

    inv["Stock_Gap_to_Reorder"] = (
        inv["Reorder_Level"] - inv["Stock_Units"]
    ).clip(lower=0)

    inv["Suggested_Reorder_Qty"] = (
        inv["Reorder_Level"] + inv["Safety_Stock"] - inv["Stock_Units"]
    ).clip(lower=0)

    inv["Inventory_Status"] = np.select(
        [
            inv["Stock_Units"] <= inv["Safety_Stock"],
            inv["Stock_Units"] <= inv["Reorder_Level"],
        ],
        [
            "Critical - Reorder Immediately",
            "Reorder Required",
        ],
        default="Healthy",
    )

    recommendations = inv.sort_values(
        ["Inventory_Status", "Suggested_Reorder_Qty"],
        ascending=[True, False],
    )

    recommendations.to_csv(
        OUTPUT_DIR / "inventory_optimization.csv", index=False
    )

    summary = (
        recommendations.groupby("Inventory_Status")
        .size()
        .reset_index(name="Count")
    )
    summary.to_csv(
        OUTPUT_DIR / "inventory_status_summary.csv", index=False
    )

    print(summary.to_string(index=False))


def create_business_insights(data, master):
    """Write a concise text report for the project presentation."""
    total_orders = master["Order_ID"].nunique()
    on_time = master["On_Time_Delivery"].eq("On Time").mean() * 100
    avg_delay = master["Delay_Days"].mean()
    top_product = (
        master.groupby("Product_Name")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )
    worst_supplier = (
        master.groupby("Supplier_Name")["Delay_Days"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )

    report = f"""
SUPPLY CHAIN VISIBILITY & OPTIMIZATION - PROJECT INSIGHTS

Total unique orders: {total_orders:,}
On-time delivery: {on_time:.2f}%
Average shipment delay: {avg_delay:.2f} days
Highest-demand product: {top_product}
Supplier with highest average delay: {worst_supplier}

RECOMMENDATIONS
1. Monitor suppliers with consistently high average delay.
2. Maintain safety stock for products with high demand.
3. Trigger replenishment when inventory reaches the reorder level.
4. Track on-time delivery and lead time by supplier and warehouse.
5. Use the demand forecast as a planning baseline and update it as new data arrives.
"""
    (OUTPUT_DIR / "business_insights.txt").write_text(
        report.strip(), encoding="utf-8"
    )


# -----------------------------
# 7. MAIN PIPELINE
# -----------------------------
def main():
    print("=" * 60)
    print("SUPPLY CHAIN VISIBILITY & OPTIMIZATION")
    print("=" * 60)

    data = load_data()
    data = prepare_dates(data)
    data = clean_data(data)

    master = build_master(data)
    master.to_csv(
        OUTPUT_DIR / "supply_chain_master.csv", index=False
    )

    run_eda(data, master)
    forecast_demand(data, periods=3)
    optimize_inventory(data)
    create_business_insights(data, master)

    print("\n=== PROJECT COMPLETED ===")
    print(f"All outputs are available in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
