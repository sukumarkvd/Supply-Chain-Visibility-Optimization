CREATE DATABASE IF NOT EXISTS supply_chain;
USE supply_chain;

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `Product_ID` VARCHAR(255),
  `Product_Name` VARCHAR(255),
  `Category` VARCHAR(255),
  `Unit_Price` DECIMAL(18,2),
  `Unit_Weight_Kg` DECIMAL(18,2),
  `Supplier_ID` VARCHAR(255),,
  PRIMARY KEY (`Product_ID`)
);

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `Order_ID` VARCHAR(255),
  `Order_Date` VARCHAR(255),
  `Customer_ID` VARCHAR(255),
  `Product_ID` VARCHAR(255),
  `Warehouse_ID` VARCHAR(255),
  `Quantity` INT,
  `Priority` VARCHAR(255),
  `Order_Status` VARCHAR(255),
  `Unit_Price` DECIMAL(18,2),
  `Order_Value` DECIMAL(18,2),,
  PRIMARY KEY (`Order_ID`)
);

DROP TABLE IF EXISTS `shipments`;
CREATE TABLE `shipments` (
  `Shipment_ID` VARCHAR(255),
  `Order_ID` VARCHAR(255),
  `Supplier_ID` VARCHAR(255),
  `Origin_Warehouse_ID` VARCHAR(255),
  `Destination_City` VARCHAR(255),
  `Shipping_Mode` VARCHAR(255),
  `Shipping_Date` VARCHAR(255),
  `Expected_Delivery_Date` VARCHAR(255),
  `Actual_Delivery_Date` VARCHAR(255),
  `Shipment_Status` VARCHAR(255),
  `Delay_Days` INT,
  `Freight_Cost` DECIMAL(18,2),,
  PRIMARY KEY (`Shipment_ID`)
);

DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory` (
  `Inventory_ID` VARCHAR(255),
  `Product_ID` VARCHAR(255),
  `Warehouse_ID` VARCHAR(255),
  `Stock_Units` INT,
  `Reorder_Level` INT,
  `Safety_Stock` INT,
  `Inventory_Date` VARCHAR(255),
  `Stock_Value` DECIMAL(18,2),,
  PRIMARY KEY (`Inventory_ID`)
);

DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE `suppliers` (
  `Supplier_ID` VARCHAR(255),
  `Supplier_Name` VARCHAR(255),
  `Country` VARCHAR(255),
  `City` VARCHAR(255),
  `Lead_Time_Days` INT,
  `Supplier_Rating` DECIMAL(18,2),
  `Unit_Cost_Index` DECIMAL(18,2),,
  PRIMARY KEY (`Supplier_ID`)
);

DROP TABLE IF EXISTS `warehouses`;
CREATE TABLE `warehouses` (
  `Warehouse_ID` VARCHAR(255),
  `Warehouse_Name` VARCHAR(255),
  `City` VARCHAR(255),
  `State` VARCHAR(255),
  `Capacity_Units` INT,,
  PRIMARY KEY (`Warehouse_ID`)
);
