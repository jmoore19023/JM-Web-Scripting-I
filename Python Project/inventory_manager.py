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

    
def view_all_products(products):  # Loops through the products list and displays each product.

    print("\n  --- All Products ---")
 
    if len(products) == 0: # Check if list is empty before attempting to display.
        print("  No products found.")
        return
 
    for product in products:
        print("  " + "-" * 40)
        product.display() # Calls display() method defined in Product class in models.py.
 
    print("  " + "-" * 40)
    print(f"  Total products: {len(products)}")
 
 
def edit_product(products):
 
    # edit_product() allows user to update fields on an existing product.
    # Searches for product by ID, displays current values, then prompts for new ones.
    # Takes one parameter: products list.
    # Returns nothing, modifies the product object directly in the list.
 
    print("\n  --- Edit Product ---")
 
    product_id = input("  Enter product ID to edit: ").strip().upper()
 
    # Search for the product in the list by ID.
    target = None
    for product in products:
        if product.product_id == product_id:
            target = product
            break
 
    if target == None: # If no match found, return to menu.
        print("  Product not found. Returning to menu.")
        return
 
    # Display current values so user knows what they are changing.
    print("\n  Current product details:")
    target.display()
 
    # Each field is optional to change. Pressing enter skips and keeps current value.
    print("\n  Press enter to keep current value.")
 
    name = input(f"  Name [{target.name}]: ").strip()
    if name != "":
        target.name = name
 
    category = input(f"  Category [{target.category}]: ").strip()
    if category != "":
        target.category = category
 
    # Quantity validation - must be a whole number and not negative.
    quantity_input = input(f"  Quantity [{target.quantity}]: ").strip()
    if quantity_input != "":
        while True:
            try:
                quantity = int(quantity_input)
                if quantity < 0:
                    print("  Quantity cannot be negative. Please try again.")
                    quantity_input = input(f"  Quantity [{target.quantity}]: ").strip()
                else:
                    target.quantity = quantity
                    break
            except ValueError:
                print("  Please enter a whole number.")
                quantity_input = input(f"  Quantity [{target.quantity}]: ").strip()
 
    # Reorder level validation - must be a whole number and not negative.
    reorder_level_input = input(f"  Reorder Level [{target.reorder_level}]: ").strip()
    if reorder_level_input != "":
        while True:
            try:
                reorder_level = int(reorder_level_input)
                if reorder_level < 0:
                    print("  Reorder level cannot be negative. Please try again.")
                    reorder_level_input = input(f"  Reorder Level [{target.reorder_level}]: ").strip()
                else:
                    target.reorder_level = reorder_level
                    break
            except ValueError:
                print("  Please enter a whole number.")
                reorder_level_input = input(f"  Reorder Level [{target.reorder_level}]: ").strip()
 
    # Price validation - must be a number and not negative.
    price_input = input(f"  Price [${target.price:.2f}]: ").strip()
    if price_input != "":
        while True:
            try:
                price = float(price_input)
                if price < 0:
                    print("  Price cannot be negative. Please try again.")
                    price_input = input(f"  Price [${target.price:.2f}]: ").strip()
                else:
                    target.price = price
                    break
            except ValueError:
                print("  Please enter a valid price (e.g. 2.99).")
                price_input = input(f"  Price [${target.price:.2f}]: ").strip()
 
    # Optional clearance date update.
    update_clearance = input("  Update clearance info? (yes/no): ").strip().lower()
    if update_clearance == "yes":
        target.clearance_date = input("  Enter clearance date (YYYY-MM-DD): ").strip()
        while True:
            try:
                target.clearance_price = float(input("  Enter clearance price: $"))
                if target.clearance_price < 0:
                    print("  Clearance price cannot be negative. Please try again.")
                else:
                    break
            except ValueError:
                print("  Please enter a valid price (e.g. 1.99).")
 
    print(f"\n  Product '{target.name}' updated successfully.")
 
 
def deactivate_product(products):
 
    # deactivate_product() sets a products active status to False.
    # We deactivate instead of delete to preserve purchase order history.
    # Takes one parameter: products list.
    # Returns nothing, modifies the active field on the product object directly.
 
    print("\n  --- Deactivate Product ---")
 
    product_id = input("  Enter product ID to deactivate: ").strip().upper()
 
    # Search for the product by ID.
    target = None
    for product in products:
        if product.product_id == product_id:
            target = product
            break
 
    if target == None: # Product not found, return to menu.
        print("  Product not found. Returning to menu.")
        return
 
    if target.active == False: # Check if already deactivated to prevent duplicate action.
        print("  This product is already deactivated.")
        return
 
    target.active = False # Set active to False to deactivate the product.
    print(f"\n  Product '{target.name}' has been deactivated.")
 
 
def view_low_stock(products):
 
    # view_low_stock() scans all products and displays any where quantity is at or below reorder level.
    # Takes one parameter: products list.
    # Returns nothing, prints all low stock products or message if none found.
 
    print("\n  --- Low Stock Products ---")
 
    low_stock = [] # Empty list to store products that are low on stock.
 
    for product in products:
        if product.quantity <= product.reorder_level: # Check if quantity is at or below reorder level.
            low_stock.append(product)
 
    if len(low_stock) == 0: # No low stock items found.
        print("  All products are sufficiently stocked.")
        return
 
    for product in low_stock:
        print("  " + "-" * 40)
        product.display()
 
    print("  " + "-" * 40)
    print(f"  Total low stock items: {len(low_stock)}")