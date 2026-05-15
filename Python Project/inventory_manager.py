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


# Product section contains all functions for managing products in the inventory.
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

    
def view_all_products(products):  

    # Loops through the products list and displays each product.

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
 
    # edit_product() allows user to update fields on an existing product. Searches for product by ID, displays current values, then prompts for new ones.
 
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
 
    # deactivate_product() sets a products active status to False. Deactivate instead of delete to preserve purchase order history.

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
 
    print("\n  --- Low Stock Products ---")
 
    low_stock = [] # Empty list to store products that are low on stock.
 
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

def view_inactive_products(products):

    # view_inactive_products() displays all products that have been deactivated.
    # Separated from active inventory to keep the main product list clean and relevant.

    print("\n  --- Inactive Products ---")

    inactive = [] # Empty list to store inactive products.

    for product in products:
        if product.active == False: # Only collect deactivated products.
            inactive.append(product)

    if len(inactive) == 0:
        print("  No inactive products found.")
        return

    for product in inactive:
        print("  " + "-" * 40)
        product.display()

    print("  " + "-" * 40)
    print(f"  Total inactive products: {len(inactive)}")


# Vendor section contains all functions that allow the user to add, view, edit, and search vendors.
# Vendor functions follow a similar pattern to product functions with input validation and searching by vendor IDs.

def add_vendor(vendors):
 
    # add_vendor() walks the user through adding a new vendor to the system. Validates all input before creating the vendor to prevent bad data.
 
    print("\n  --- Add New Vendor ---")
 
    # Vendor ID must be unique. Checks for existing vendor ID before accepting it.
 
    vendor_id = input("  Enter vendor ID (e.g. V001): ").strip().upper()
 
    for vendor in vendors:
        if vendor.vendor_id == vendor_id:
            print("  A vendor with that ID already exists. Returning to menu.")
            return
 
    name = input("  Enter vendor business name: ").strip() # Validation to prevent empty vendor name.
    if name == "":
        print("  Vendor name cannot be empty. Returning to menu.")
        return
 
    contact_name = input("  Enter contact name: ").strip() # Validation to prevent empty contact name.
    if contact_name == "":
        print("  Contact name cannot be empty. Returning to menu.")
        return
 
    phone = input("  Enter phone number: ").strip() # Validation to prevent empty phone number.
    if phone == "":
        print("  Phone number cannot be empty. Returning to menu.")
        return
 
    email = input("  Enter email address: ").strip() # Validation to prevent empty email address.
    if email == "":
        print("  Email address cannot be empty. Returning to menu.")
        return
 
    address = input("  Enter city/state or address: ").strip() # Validation to prevent empty address.
    if address == "":
        print("  Address cannot be empty. Returning to menu.")
        return
 
    # Create the new Vendor object and add it to the list.
 
    new_vendor = Vendor(
        vendor_id=vendor_id,
        name=name,
        contact_name=contact_name,
        phone=phone,
        email=email,
        address=address
    )
 
    vendors.append(new_vendor)
    print(f"\n  Vendor '{name}' added successfully.")
 
 
def view_all_vendors(vendors):
 
    # view_all_vendors() loops through the vendors list and displays each vendor.
 
    print("\n  --- All Vendors ---")
 
    if len(vendors) == 0: # Check if list is empty before attempting to display.
        print("  No vendors found.")
        return
 
    for vendor in vendors:
        print("  " + "-" * 40)
        vendor.display() # Calls display() method defined in Vendor class in models.py.
 
    print("  " + "-" * 40)
    print(f"  Total vendors: {len(vendors)}")
 
 
def edit_vendor(vendors):
 
    # edit_vendor() allows user to update fields on an existing vendor.
    # Searches for vendor by ID, displays current values, then prompts for new ones.
 
    print("\n  --- Edit Vendor ---")
 
    vendor_id = input("  Enter vendor ID to edit: ").strip().upper()
 
    # Search for the vendor in the list by ID.
    target = None
    for vendor in vendors:
        if vendor.vendor_id == vendor_id:
            target = vendor
            break
 
    if target == None: # If no match found, return to menu.
        print("  Vendor not found. Returning to menu.")
        return
 
    # Display current values so user knows what they are changing.
    print("\n  Current vendor details:")
    target.display()
 
    # Each field is optional to change. Pressing enter skips and keeps current value.
    print("\n  Press enter to keep current value.")
 
    name = input(f"  Business Name [{target.name}]: ").strip()
    if name != "":
        target.name = name
 
    contact_name = input(f"  Contact Name [{target.contact_name}]: ").strip()
    if contact_name != "":
        target.contact_name = contact_name
 
    phone = input(f"  Phone [{target.phone}]: ").strip()
    if phone != "":
        target.phone = phone
 
    email = input(f"  Email [{target.email}]: ").strip()
    if email != "":
        target.email = email
 
    address = input(f"  Address [{target.address}]: ").strip()
    if address != "":
        target.address = address
 
    print(f"\n  Vendor '{target.name}' updated successfully.")
 
 
def search_vendors(vendors):
 
    # search_vendors() searches the vendors list by name or ID and displays matches.

    print("\n  --- Search Vendors ---")
 
    search_term = input("  Enter vendor name or ID to search: ").strip().upper()
 
    results = [] # Empty list to store matching vendors.
 
    for vendor in vendors:
        # Check if search term matches vendor ID or appears in vendor name.
        if vendor.vendor_id == search_term or search_term in vendor.name.upper():
            results.append(vendor)
 
    if len(results) == 0: # No matching vendors found.
        print("  No vendors found matching that search.")
        return
 
    for vendor in results:
        print("  " + "-" * 40)
        vendor.display()
 
    print("  " + "-" * 40)
    print(f"  {len(results)} vendor(s) found.")

# Search section contains functions for searching products and vendors by different fields. 
# Each search function follows the same pattern by looping, matching, collecting, and then displaying the results.

 
def search_by_product_id(products):
 
    # search_by_product_id() searches the products list for an exact match on product ID.
    # Exact match used because product IDs are unique identifiers.
    # Takes one parameter: products list.
    # Returns nothing, prints matching product or message if not found.
 
    print("\n  --- Search by Product ID ---")
 
    search_term = input("  Enter product ID to search: ").strip().upper()
 
    results = [] # Empty list to store matching products.
 
    for product in products:
        if product.product_id == search_term: # Exact match on product ID.
            results.append(product)
 
    if len(results) == 0: # No matching products found.
        print("  No products found matching that ID.")
        return
 
    for product in results:
        print("  " + "-" * 40)
        product.display()
 
    print("  " + "-" * 40)
    print(f"  {len(results)} product(s) found.")
 
 
def search_by_name(products):
 
    # search_by_name() searches the products list for a partial match on product name.
    # Partial match used so user can search part of a name and still find results.
    # Takes one parameter: products list.
    # Returns nothing, prints all matching products or message if none found.
 
    print("\n  --- Search by Product Name ---")
 
    search_term = input("  Enter product name to search: ").strip().upper()
 
    results = [] # Empty list to store matching products.
 
    for product in products:
        if search_term in product.name.upper(): # Partial match on product name.
            results.append(product)
 
    if len(results) == 0: # No matching products found.
        print("  No products found matching that name.")
        return
 
    for product in results:
        print("  " + "-" * 40)
        product.display()
 
    print("  " + "-" * 40)
    print(f"  {len(results)} product(s) found.")
 
def search_by_category(products):

    # search_by_category() searches the products list for a partial match on category.
    # Partial match used so user can search part of a category name and find all related products.

    print("\n  --- Search by Category ---")

    search_term = input("  Enter category to search: ").strip().upper()

    results = [] # Empty list to store matching products.

    for product in products:
        if search_term in product.category.upper(): # Partial match on category.
            results.append(product)

    if len(results) == 0: # No matching products found.
        print("  No products found in that category.")
        return

    for product in results:
        print("  " + "-" * 40)
        product.display()

    print("  " + "-" * 40)
    print(f"  {len(results)} product(s) found.")


def search_by_vendor(products):

    # search_by_vendor() searches the products list for an exact match on vendor ID.
    # Exact match used because vendor IDs are unique identifiers.
    # One to many relationship means multiple products can share the same vendor ID.

    print("\n  --- Search by Vendor ID ---")

    search_term = input("  Enter vendor ID to search: ").strip().upper()

    results = [] # Empty list to store matching products.

    for product in products:
        if product.vendor_id == search_term: # Exact match on vendor ID and adds to product list.
            results.append(product)

    if len(results) == 0: 
        print("  No products found for that vendor.")
        return

    for product in results:
        print("  " + "-" * 40)
        product.display()

    print("  " + "-" * 40)
    print(f"  {len(results)} product(s) found.")

# Sort section below contains functions for sorting products by different fields.
# Helper functions are used to tell sorted() which field to compare on each product object.

def get_name(product): # Function that sorted() uses to compare product names when sorting by name.
    
    return product.name

def get_quantity(product): # Function that sorted() uses to compare product quantities when sorting by quantity.

    return product.quantity

def get_price(product): # Function that sorted() uses to compare product prices when sorting by price.

    return product.price

def sort_by_name(products):

    # sort_by_name() sorts the products list alphabetically by product name A to Z.

    print("\n  --- Products Sorted by Name ---")

    if len(products) == 0: 
        print("  No products found.")
        return

    sorted_list = sorted(products, key=get_name) # Create sorted copy using get_name() as the key.

    for product in sorted_list:
        print("  " + "-" * 40)
        product.display()

    print("  " + "-" * 40)
    print(f"  Total products: {len(sorted_list)}")


def sort_by_quantity(products):

    # sort_by_quantity() sorts the products list from in ascending order by quantity in stock.

    print("\n  --- Products Sorted by Quantity ---")

    if len(products) == 0: 
        print("  No products found.")
        return

    sorted_list = sorted(products, key=get_quantity) # Create sorted copy using get_quantity() as the key.

    for product in sorted_list:
        print("  " + "-" * 40)
        product.display()

    print("  " + "-" * 40)
    print(f"  Total products: {len(sorted_list)}")


def sort_by_price(products):

    # sort_by_price() sorts the products list in ascending order by unit price.

    print("\n  --- Products Sorted by Price ---")

    if len(products) == 0:
        print("  No products found.")
        return

    sorted_list = sorted(products, key=get_price) # Create sorted copy using get_price() as the key.

    for product in sorted_list:
        print("  " + "-" * 40)
        product.display()

    print("  " + "-" * 40)
    print(f"  Total products: {len(sorted_list)}")

# Purchase Order section contains functions for creating and viewing purchase orders.
# Purchase orders connect vendors and products together into a single transaction record.
# This section is what creates associations between all the different parts of the program.

def create_purchase_order(products, vendors, purchase_orders):

    # create_purchase_order() walks user through building a purchase order with a vendor and products.
    # Takes three parameters: products list, vendors list, and purchase_orders list. (Essentially the rest of program)

    print("\n  --- Create Purchase Order ---")

    # Generate unique PO number based on how many orders already exist.
    next_number = len(purchase_orders) + 1
    po_number = "PO" + str(next_number)

    # Ask for vendor ID and validate it exists in the vendors list.
    vendor_id = input("  Enter vendor ID: ").strip().upper()

    target_vendor = None # Search for vendor by ID.
    for vendor in vendors:
        if vendor.vendor_id == vendor_id:
            target_vendor = vendor
            break

    if target_vendor == None:
        print("  Vendor not found. Please add the vendor first. Returning to menu.")
        return

    print(f"  Vendor: {target_vendor.name}") # Confirm vendor name to user.

    # Display all active products for reference before user starts adding items.
    print("\n  Available Products:")
    print("  " + "-" * 40)
    for product in products:
        if product.active == True: # Only show active products.
            print(f"  {product.product_id} - {product.name} - ${product.price:.2f}")
    print("  " + "-" * 40)

    items = [] # Empty list to store items added to this order.
    total_cost = 0 # Running total updated as each item is added.

    # Loop allows user to keep adding products until they are done.
    while True:

        product_id = input("\n  Enter product ID to add to order: ").strip().upper()

        # Search for the product in the products list.
        target_product = None
        for product in products:
            if product.product_id == product_id:
                target_product = product
                break

        if target_product == None:
            print("  Product not found. Please try again.")
            continue

        if target_product.active == False:
            print("  This product is inactive and cannot be ordered.")
            continue

        # Quantity validation - must be a whole number greater than zero.
        while True:
            try:
                quantity = int(input("  Enter quantity to order: "))
                if quantity <= 0:
                    print("  Quantity must be greater than zero. Please try again.")
                else:
                    break
            except ValueError:
                print("  Please enter a whole number.")

        # Calculate line total and update running total.
        line_total = quantity * target_product.price
        total_cost = total_cost + line_total

        # Build item dictionary and add to items list.
        item = {
            "product_id": target_product.product_id,
            "product_name": target_product.name,
            "quantity": quantity,
            "unit_price": target_product.price
        }
        items.append(item)

        print(f"  Added: {target_product.name} x{quantity} @ ${target_product.price:.2f} each")
        print(f"  Running total: ${total_cost:.2f}")

        # Ask if user wants to add another product or finish the order.
        another = input("\n  Add another product? (yes/no): ").strip().lower()
        if another != "yes":
            break

    # Check that at least one item was added before continuing.
    if len(items) == 0:
        print("  No items were added. Purchase order cancelled.")
        return

    # Show full order summary for user to review before confirming.
    print("\n  --- Order Summary ---")
    print(f"  PO Number : {po_number}")
    print(f"  Vendor    : {target_vendor.name}")
    print(f"  Items     :")
    for item in items:
        line = item["quantity"] * item["unit_price"]
        print(f"    - {item['product_name']} x{item['quantity']} @ ${item['unit_price']:.2f} = ${line:.2f}")
    print(f"  Total     : ${total_cost:.2f}")
    print("  " + "-" * 40)

    # Ask user to confirm before creating the purchase order.
    confirm = input("  Confirm order? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Purchase order cancelled. Returning to menu.")
        return

    # Stamp todays date automatically using the date module imported at the top.
    date_created = str(date.today())

    # Create the PurchaseOrder object and add it to the list.
    new_order = PurchaseOrder(
        po_number=po_number,
        vendor_id=vendor_id,
        date_created=date_created,
        items=items,
        total_cost=total_cost,
        status="Open"
    )

    purchase_orders.append(new_order)
    print(f"\n  Purchase Order {po_number} created successfully.")
    print(f"  Vendor: {target_vendor.name}")
    print(f"  Items : {len(items)}")
    print(f"  Total : ${total_cost:.2f}")

def view_purchase_orders(purchase_orders):

    # view_purchase_orders() displays purchase orders filtered by status.
    # Allows user to view open orders, received orders, or all orders.

    print("\n  --- View Purchase Orders ---")

    if len(purchase_orders) == 0:
        print("  No purchase orders found.")
        return

    # Ask user which orders they want to see.
    print("  Filter by status:")
    print("    1. Open orders only")
    print("    2. Received orders only")
    print("    3. All orders")

    choice = input("\n  Enter choice: ").strip()

    results = [] # Empty list to store matching orders.

    for order in purchase_orders:
        if choice == "1" and order.status == "Open": # Filter for open orders only.
            results.append(order)
        elif choice == "2" and order.status == "Received": # Filter for received orders only.
            results.append(order)
        elif choice == "3": # No filter, add all orders.
            results.append(order)

    if len(results) == 0:
        print("  No orders found matching that filter.")
        return

    for order in results:
        print("  " + "-" * 40)
        order.display() # Calls display() method defined in PurchaseOrder class in models.py.

    print("  " + "-" * 40)
    print(f"  {len(results)} order(s) found.")


def receive_shipment(products, purchase_orders):

    # receive_shipment() processes an incoming shipment for an open purchase order.
    # Finds the matching PO, updates inventory quantities for each item ordered and marks the order as received to prevent duplicate receiving.

    print("\n  --- Receive Shipment ---")

    # Show all open orders for reference so user knows what PO numbers are available.
    print("\n  Open Purchase Orders:")
    print("  " + "-" * 40)

    open_orders = [] # Collect open orders to display and check against.
    for order in purchase_orders:
        if order.status == "Open":
            open_orders.append(order)
            print(f"  {order.po_number} - {order.vendor_id} - {order.date_created} - ${order.total_cost:.2f}")

    if len(open_orders) == 0:
        print("  No open purchase orders found.")
        return

    print("  " + "-" * 40)

    # Ask for PO number to receive.
    po_number = input("\n  Enter PO number to receive: ").strip().upper()

    # Search for the purchase order by PO number.
    target_order = None
    for order in purchase_orders:
        if order.po_number == po_number:
            target_order = order
            break

    if target_order == None:
        print("  Purchase order not found. Returning to menu.")
        return

    # Check if order has already been received to prevent duplicate receiving.
    if target_order.status == "Received":
        print("  This order has already been received. Returning to menu.")
        return

    # Show order details so user can confirm before updating inventory.
    print("\n  Order details:")
    target_order.display()

    # Ask user to confirm before updating inventory.
    confirm = input("\n  Confirm receiving this shipment? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Receiving cancelled. Returning to menu.")
        return

    # Loop through each item in the order and update matching product quantity.
    # Two loops needed - outer loop goes through order items,
    # inner loop searches products list to find the matching product.

    for item in target_order.items:
        for product in products:
            if product.product_id == item["product_id"]: # Match found, update quantity.
                product.quantity = product.quantity + item["quantity"]
                print(f"  Updated: {product.name} - new quantity: {product.quantity}")
                break

    # Mark order as received to prevent it from being received again.
    target_order.status = "Received"

    print(f"\n  Shipment for {target_order.po_number} received successfully.")
    print(f"  {len(target_order.items)} product(s) updated in inventory.")
