# =============================================================================
# file_manager.py
# Moore Plants and Pots - Inventory and Purchase Order System
# Created by: John Moore
# Created on: 2026-05-12
#
# PURPOSE:
# This file is responsible for saving and loading all program data to and from a JSON file.
# All file handling is done here and solves the problem of data persistence.
# Without this file, all products, vendors, and purchase order history would be lost every time the program closes.
# 
#
# This file acts as the memory of the program. It uses the to_dict() and
# from_dict() methods defined in models.py to convert objects to and from
# a format that can be stored in a JSON file.
#
# =============================================================================

import json
# json module used for reading and writing JSON files.

import os
# os module used to interact with the operating system.

from models import Product, Vendor, PurchaseOrder
# Import the three classes from models.py
# Use the from_dict() to convert loaded data back into usable objects.


DATA_FILE = "store_data.json"
# Constant variable for the name of JSON file where all data is stored. 
# Storing in variable allows it to be changed throughout entire file in one change.

def save_data(products, vendors, purchase_orders):

    # save_data() function takes all three lists of objects and writes them to the JSON file.
    # Function takes three parameters: products, vendors, and purchase_orders.
    # Objects are then converted to dictionaries and packaged into one combined dictionary before written to file.

    # Objects here are converted to dictionaries using it's own to_dict() method.
    products_data = []
    for product in products:
        products_data.append(product.to_dict())

    vendors_data = []
    for vendor in vendors:
        vendors_data.append(vendor.to_dict())

    orders_data = []
    for order in purchase_orders:
        orders_data.append(order.to_dict())

    # The 3 dictionaries above are now packed into a single dictionary that can be unpacked later by the load_data() function.

    all_data = {
        "products": products_data,
        "vendors": vendors_data,
        "purchase_orders": orders_data
    }

    # Write the combined dictionary to the JSON file.
    # Error handling included to catch any issues while saving file.

    try:
        with open(DATA_FILE, "w") as file:
            
            json.dump(all_data, file, indent=4) #Indent 4 added for readability when opened in editor.

        print("  Data saved successfully.")

    except Exception as error:
        print(f"  Error saving data: {error}") #Exception error to notify user if save fails.


def load_data():

    # load_data() function reads the JSON file and converts everything back into objects for Python to use.
    # Effectively the reverse of the save_data() function. Called when the program starts and loads saved data.
    # os.path module checks first and handles the case when files doesn't exist.

    if os.path.exists(DATA_FILE) == False: # Return three empty lists so the program starts fresh without crashing
 
        print("  No saved data found. Starting with empty inventory.")
        return [], [], []

    # Open and read the file. Try/except to handle unreadable file.

    try:
        with open(DATA_FILE, "r") as file:

            all_data = json.load(file)

        # Convert dictionaries back into objects and stores into three separate lists.
        # from_dict() used to convert dictionaries back into correct object class.

        products = []
        for item in all_data.get("products", []):
            products.append(Product.from_dict(item))

        vendors = []
        for item in all_data.get("vendors", []):
            vendors.append(Vendor.from_dict(item))

        purchase_orders = []
        for item in all_data.get("purchase_orders", []):
            purchase_orders.append(PurchaseOrder.from_dict(item))

        print(f"  Data loaded successfully.")
        print(f"  {len(products)} products, {len(vendors)} vendors, {len(purchase_orders)} purchase orders loaded.")
        
        return products, vendors, purchase_orders

    except Exception as error: # Catch exceptions that occur during file reading/loading process.
    
        print(f"  Error loading data: {error}")
        return [], [], []

def initialize_data():

    # initialize_data() called in main.py when program starts. Calls load_data() and returns results.
    # If no file exists, load_data() handles that and returns empty lists.

    return load_data()