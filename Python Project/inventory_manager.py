# =============================================================================
# inventory_manager.py
# Moore Plants and Pots - Inventory and Purchase Order System
# Created by: John Moore
# Created on: 2026-05-12
#
# PURPOSE:
# This file is the core part of the program and contains all the main functions.
# It contains the logic for managing products, vendors, purchase orders, and shipments.
# Every meaningful action a user can take runs through a function in this file.
# main.py will handle the user interface and menu navigation with this file handling the actual logic
# =============================================================================

from models import Product, Vendor, PurchaseOrder
# Import classes from models.py to create and manipulate objects in this file.

from datetime import date
# Python module used to automatically implement dates for orders and shipments.



# Section contains all functions for managing products in the inventory.
# Functions here allow the user to add, view, edit, deactivate, and check stock levels for products.

def add_product(products, vendors):


    # add_product() walks the user through adding a new product to inventory.
    # Validates all input before creating the product to prevent bad data.

    print("\n  --- Add New Product ---")

    # Product ID must be unique. Checks for existing product ID before accepting it.

    product_id = input("  Enter product ID (e.g. P001): ").strip().upper()

    for product in products:
        if product.product_id == product_id:
            print("  A product with that ID already exists. Returning to menu.")
            return



    name = input("  Enter product name: ").strip() # Validation to prevent empty product name.
    if name == "":
        print("  Product name cannot be empty. Returning to menu.")
        return

    category = input("  Enter category (e.g. Seeds, Tools, Soil): ").strip() # Validation to prevent empty category name.
    if category == "":
        print("  Category cannot be empty. Returning to menu.")
        return


    while True: #Validation to ensure quantity is a valid value.
        try:
            quantity = int(input("  Enter quantity in stock: "))
            if quantity < 0:
                print("  Quantity cannot be negative. Please try again.")
            else:
                break
        except ValueError:
            print("  Please enter a whole number.")


    while True: #Validation to ensure reorder level is a valid value and not negative.
        try:
            reorder_level = int(input("  Enter reorder level: "))
            if reorder_level < 0:
                print("  Reorder level cannot be negative. Please try again.")
            else:
                break
        except ValueError:
            print("  Please enter a whole number.")


    while True: # Validation to ensure is greater than zero and whole number.
        try:
            reorder_quantity = int(input("  Enter reorder quantity: "))
            if reorder_quantity <= 0:
                print("  Reorder quantity must be greater than zero. Please try again.")
            else:
                break
        except ValueError:
            print("  Please enter a whole number.")


    while True: # Validation for numbers that are negative and non-numeric.
        try:
            price = float(input("  Enter unit price: $"))
            if price < 0:
                print("  Price cannot be negative. Please try again.")
            else:
                break
        except ValueError:
            # Catches non-numeric input
            print("  Please enter a valid price (e.g. 2.99).")

    # Get and validate vendor ID. Must match an existing vendor in the vendors list.

    vendor_id = input("  Enter vendor ID: ").strip().upper()


    vendor_found = False # Check that the vendor ID exists in our vendors list
    for vendor in vendors:
        if vendor.vendor_id == vendor_id:
            vendor_found = True
            break

    if vendor_found == False:
        print("  Vendor ID not found. Please add the vendor first. Returning to menu.")
        return

    # Optional clearance date and price for products that are on clearance.

    clearance_date = None
    clearance_price = None

    add_clearance = input("  Does this product have a clearance date? (yes/no): ").strip().lower()

    if add_clearance == "yes":

        clearance_date = input("  Enter clearance date (YYYY-MM-DD): ").strip()

        while True:
            try:
                clearance_price = float(input("  Enter clearance price: $"))
                if clearance_price < 0:
                    print("  Clearance price cannot be negative. Please try again.")
                else:
                    break
            except ValueError:
                print("  Please enter a valid price (e.g. 1.99).")

    # Create the new Product object and add it to the list.

    new_product = Product(
        product_id=product_id,
        name=name,
        category=category,
        quantity=quantity,
        reorder_level=reorder_level,
        reorder_quantity=reorder_quantity,
        price=price,
        vendor_id=vendor_id,
        active=True,
        clearance_date=clearance_date,
        clearance_price=clearance_price
    )

    products.append(new_product)
    print(f"\n  Product '{name}' added successfully.")