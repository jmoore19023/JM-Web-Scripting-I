# =============================================================================
# reports.py
# Moore Plants and Pots - Inventory and Purchase Order System
# Created by: John Moore
# Created on: 2026-05-15
#
# PURPOSE:
# This file contains all reporting functions for the program.
# Reports are read only and never modify any data.
# They loop through the data lists, collect what they need, and display results.
# All functions are called from reports_menu() in main.py.
# =============================================================================

from datetime import date
# date module used to compare clearance dates against todays date.


# Report functions below display different views of the inventory and purchase order data.
# All functions follow the same pattern - loop, collect, calculate if needed, display.

def full_inventory_report(products):

    # full_inventory_report() displays all products in the system regardless of status.

    print("\n  --- Full Inventory Report ---")

    if len(products) == 0:
        print("  No products found.")
        return

    for product in products:
        print("  " + "-" * 40)
        product.display() # Calls display() method from Product class in models.py.

    print("  " + "-" * 40)
    print(f"  Total products in system: {len(products)}")


def low_stock_report(products):

    # low_stock_report() displays all products where quantity is at or below reorder level.

    print("\n  --- Low Stock Report ---")

    low_stock = [] # Empty list to store low stock products.

    for product in products:
        if product.quantity <= product.reorder_level: # Check if quantity is at or below reorder level.
            low_stock.append(product)

    if len(low_stock) == 0:
        print("  All products are sufficiently stocked.")
        return

    for product in low_stock:
        print("  " + "-" * 40)
        product.display()

    print("  " + "-" * 40)
    print(f"  Total low stock items: {len(low_stock)}")


def inventory_value_report(products):

    # inventory_value_report() calculates and displays the total value of all stock.
    # Value is calculated by multiplying quantity by price for each product.

    print("\n  --- Inventory Value Report ---")

    if len(products) == 0:
        print("  No products found.")
        return

    total_value = 0 # Running total updated as each product value is calculated.

    for product in products:
        product_value = product.quantity * product.price # Calculate value for this product.
        total_value = total_value + product_value # Add to running total.
        print(f"  {product.name:<30} qty: {product.quantity:<6} value: ${product_value:.2f}")

    print("  " + "-" * 40)
    print(f"  Total Inventory Value: ${total_value:.2f}")


def open_purchase_orders_report(purchase_orders):

    # open_purchase_orders_report() displays all purchase orders with Open status.

    print("\n  --- Open Purchase Orders Report ---")

    open_orders = [] # Empty list to store open purchase orders.

    for order in purchase_orders:
        if order.status == "Open": # Only collect orders with Open status.
            open_orders.append(order)

    if len(open_orders) == 0:
        print("  No open purchase orders found.")
        return

    for order in open_orders:
        print("  " + "-" * 40)
        order.display() # Calls display() method from PurchaseOrder class in models.py.

    print("  " + "-" * 40)
    print(f"  Total open orders: {len(open_orders)}")


def received_purchase_orders_report(purchase_orders):

    # received_purchase_orders_report() displays all purchase orders with Received status.
    # Takes one parameter: purchase_orders list.
    # Returns nothing, prints all received orders or message if none found.

    print("\n  --- Received Purchase Orders Report ---")

    received_orders = [] # Empty list to store received purchase orders.

    for order in purchase_orders:
        if order.status == "Received": # Only collect orders with Received status.
            received_orders.append(order)

    if len(received_orders) == 0:
        print("  No received purchase orders found.")
        return

    for order in received_orders:
        print("  " + "-" * 40)
        order.display()

    print("  " + "-" * 40)
    print(f"  Total received orders: {len(received_orders)}")


def clearance_items_report(products):

    # clearance_items_report() displays all products that have a clearance date set.
    # Checks todays date against the clearance date to show if item is active or upcoming.
    # Takes one parameter: products list.
    # Returns nothing, prints all clearance items or message if none found.

    print("\n  --- Clearance Items Report ---")

    today = date.today() # Get todays date for comparison against clearance dates.

    clearance_items = [] # Empty list to store products with clearance dates.

    for product in products:
        if product.clearance_date != None: # Only collect products with a clearance date.
            clearance_items.append(product)

    if len(clearance_items) == 0:
        print("  No clearance items found.")
        return

    for product in clearance_items:
        print("  " + "-" * 40)
        print(f"  Product ID    : {product.product_id}")
        print(f"  Name          : {product.name}")
        print(f"  Regular Price : ${product.price:.2f}")
        print(f"  Clearance Price: ${product.clearance_price:.2f}")
        print(f"  Clearance Date: {product.clearance_date}")

        # Compare clearance date to today to show current status.
        clearance_date = date.fromisoformat(product.clearance_date) # Convert string to date for comparison.
        if clearance_date <= today:
            print(f"  Status        : Currently on clearance")
        else:
            print(f"  Status        : Clearance upcoming")

    print("  " + "-" * 40)
    print(f"  Total clearance items: {len(clearance_items)}")


def restock_cost_estimator(products):

    # restock_cost_estimator() calculates the total cost to restock all low stock items.
    # For each low stock product, calculates cost based on reorder quantity and unit price.
    # Takes one parameter: products list.
    # Returns nothing, prints restock cost per product and grand total.

    print("\n  --- Restock Cost Estimator ---")

    low_stock = [] # Empty list to store low stock products.

    for product in products:
        if product.quantity <= product.reorder_level: # Find all low stock products.
            low_stock.append(product)

    if len(low_stock) == 0:
        print("  No products currently need restocking.")
        return

    total_restock_cost = 0 # Running total of all restock costs.

    for product in low_stock:
        restock_cost = product.reorder_quantity * product.price # Cost to restock this product.
        total_restock_cost = total_restock_cost + restock_cost # Add to running total.
        print(f"  {product.name:<30} reorder qty: {product.reorder_quantity:<6} cost: ${restock_cost:.2f}")

    print("  " + "-" * 40)
    print(f"  Total Estimated Restock Cost: ${total_restock_cost:.2f}")