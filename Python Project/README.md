# Moore Plants and Pots
# Inventory and Purchase Order System
# Created by: John Moore


## Description

Moore Plants and Pots is a console based inventory and purchase order
management system built in Python. The program simulates a small business
workflow for a garden and plant supply store, allowing users to manage
products, vendors, purchase orders, and inventory through a simple menu system.


## Features

- Product management - add, view, edit, deactivate, low stock, inactive
- Vendor management - add, view, edit, search
- Purchase order creation with vendor and product validation
- Shipment receiving with duplicate prevention
- Search products by ID, name, category, and vendor
- Sort products by name, quantity, and price
- Seven reports including inventory value and restock cost estimator
- JSON save and load between sessions
- Clearance date and price tracking for seasonal items
- Restock cost estimator for low stock products


## Required Files

- main.py - user interface and menu system
- models.py - Product, Vendor, and PurchaseOrder classes
- inventory_manager.py - core business logic
- file_manager.py - save and load data
- reports.py - all reporting functions
- store_data.json - data storage


## How to Run

1. Make sure Python 3 is installed
2. Place all files in the same folder
3. Open a terminal and navigate to the project folder
4. Run the program with: python3 main.py
5. Navigate using the numbered menu options
6. Select Save and Exit to save your data before closing


## How Data is Stored

All data is saved to store_data.json between sessions.
Products, vendors, and purchase orders are converted to
dictionaries and written to the file using json.dump().
When loading, json.load() reads the file back and converts
each section into Python objects using from_dict().


## Extra Features

Clearance Date Tracker - products can have an optional clearance
date and reduced price. The clearance report shows which items
are currently on clearance or coming up for clearance.

Restock Cost Estimator - calculates the total cost to restock
all low stock items based on the units needed to reach the
reorder quantity.