# =============================================================================
# main.py
# Moore Plants and Pots - Inventory and Purchase Order System
# Created by: John Moore
# Created on: 2026-05-15
#
# PURPOSE:
# This file is the entry point and user interface for the program.
# main.py takes the user's request and connects them to the right function in the right file.
#
# =============================================================================


# Import functions from all other files.
# main.py is the only file that imports from everything.

from file_manager import initialize_data, save_data
# initialize_data() loads saved data on startup.
# save_data() writes all data to file on exit.

from inventory_manager import (
    add_product, view_all_products, edit_product,
    deactivate_product, view_low_stock, view_inactive_products,
    add_vendor, view_all_vendors, edit_vendor, search_vendors,
    search_by_product_id, search_by_name, search_by_category, search_by_vendor,
    sort_by_name, sort_by_quantity, sort_by_price,
    create_purchase_order, view_purchase_orders, receive_shipment
)

# Import all functions from inventory_manager.py.
# These handle all product, vendor, purchase order, search, and sort operations.

from reports import (
    full_inventory_report, low_stock_report, inventory_value_report,
    open_purchase_orders_report, received_purchase_orders_report,
    clearance_items_report, restock_cost_estimator
)
# Import all report functions from reports.py.


# MENU FUNCTIONS
# Each menu is its own function to keep the code organized and readable.


def product_menu(products, vendors):

    # product_menu() displays the product management submenu.
    # Parameters: products list, vendors list
    # Returns: Nothing. Loops until user selects back

    while True:

        print("\n  --- Product Management ---")
        print("  1. Add Product")
        print("  2. View All Products")
        print("  3. Edit Product")
        print("  4. Deactivate Product")
        print("  5. View Low Stock")
        print("  6. View Inactive Products")
        print("  7. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            add_product(products, vendors)
        elif choice == "2":
            view_all_products(products)
        elif choice == "3":
            edit_product(products)
        elif choice == "4":
            deactivate_product(products)
        elif choice == "5":
            view_low_stock(products)
        elif choice == "6":
            view_inactive_products(products)
        elif choice == "7":
            break # Return to main menu.
        else:
            print("  Invalid choice. Please enter a number from the menu.")


def vendor_menu(vendors):

    # vendor_menu() displays the vendor management submenu.
    # Parameters: vendors list
    # Returns: Nothing. Loops until user selects back

    while True:

        print("\n  --- Vendor Management ---")
        print("  1. Add Vendor")
        print("  2. View All Vendors")
        print("  3. Edit Vendor")
        print("  4. Search Vendors")
        print("  5. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            add_vendor(vendors)
        elif choice == "2":
            view_all_vendors(vendors)
        elif choice == "3":
            edit_vendor(vendors)
        elif choice == "4":
            search_vendors(vendors)
        elif choice == "5":
            break # Return to main menu.
        else:
            print("  Invalid choice. Please enter a number from the menu.")


def purchase_order_menu(products, vendors, purchase_orders):

    # purchase_order_menu() displays the purchase order submenu.
    # Parameters: products list, vendors list, purchase_orders list
    # Returns: nothing. Loops until user selects back

    while True:

        print("\n  --- Purchase Orders ---")
        print("  1. Create Purchase Order")
        print("  2. View Purchase Orders")
        print("  3. Receive Shipment")
        print("  4. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            create_purchase_order(products, vendors, purchase_orders)
        elif choice == "2":
            view_purchase_orders(purchase_orders)
        elif choice == "3":
            receive_shipment(products, purchase_orders)
        elif choice == "4":
            break # Return to main menu.
        else:
            print("  Invalid choice. Please enter a number from the menu.")


def search_menu(products):

    # search_menu() displays the product search submenu.
    # Parameters: products list
    # Returns: Nothing. Loops until user selects back

    while True:

        print("\n  --- Search Products ---")
        print("  1. Search by Product ID")
        print("  2. Search by Name")
        print("  3. Search by Category")
        print("  4. Search by Vendor ID")
        print("  5. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            search_by_product_id(products)
        elif choice == "2":
            search_by_name(products)
        elif choice == "3":
            search_by_category(products)
        elif choice == "4":
            search_by_vendor(products)
        elif choice == "5":
            break # Return to main menu.
        else:
            print("  Invalid choice. Please enter a number from the menu.")


def sort_menu(products):

    # sort_menu() displays the product sort submenu.
    # Parameters: products list
    # Returns: Nothing. Loops until user selects back

    while True:

        print("\n  --- Sort Products ---")
        print("  1. Sort by Name")
        print("  2. Sort by Quantity")
        print("  3. Sort by Price")
        print("  4. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            sort_by_name(products)
        elif choice == "2":
            sort_by_quantity(products)
        elif choice == "3":
            sort_by_price(products)
        elif choice == "4":
            break # Return to main menu.
        else:
            print("  Invalid choice. Please enter a number from the menu.")


def reports_menu(products, purchase_orders):

    # reports_menu() displays the reports submenu.
    # Parameters: products list, purchase_orders list
    # Returns: Nothing. Loops until user selects back.

    while True:

        print("\n  --- Reports ---")
        print("  1. Full Inventory Report")
        print("  2. Low Stock Report")
        print("  3. Inventory Value Report")
        print("  4. Open Purchase Orders Report")
        print("  5. Received Purchase Orders Report")
        print("  6. Clearance Items Report")
        print("  7. Restock Cost Estimator")
        print("  8. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            full_inventory_report(products)
        elif choice == "2":
            low_stock_report(products)
        elif choice == "3":
            inventory_value_report(products)
        elif choice == "4":
            open_purchase_orders_report(purchase_orders)
        elif choice == "5":
            received_purchase_orders_report(purchase_orders)
        elif choice == "6":
            clearance_items_report(products)
        elif choice == "7":
            restock_cost_estimator(products)
        elif choice == "8":
            break # Return to main menu.
        else:
            print("  Invalid choice. Please enter a number from the menu.")



# This is where the program starts. Loads data, shows main menu, saves on exit.
# Functions above are what get called from the main menu. Each function is a submenu, which all act in the same manner.


def main():

    # main() is the entry point for the program.
    # Loads data on startup, runs the main menu loop, saves data on exit.
    # Parameters: none
    # Returns: Nothing. Runs until user saves and exits

    print("\n  ============================================")
    print("       Welcome to Moore Plants and Pots      ")
    print("      Inventory and Purchase Order System  ")
    print("  ============================================")

    # Load saved data on startup using initialize_data() from file_manager.py.
    # Returns three lists that get passed around to every function that needs them.
    
    products, vendors, purchase_orders = initialize_data()

    # Main menu loop runs until user chooses to save and exit.
    while True:

        print("\n  --- Main Menu ---")
        print("  1. Product Management")
        print("  2. Vendor Management")
        print("  3. Purchase Orders")
        print("  4. Search Products")
        print("  5. Sort Products")
        print("  6. Reports")
        print("  7. Save and Exit")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            product_menu(products, vendors)
        elif choice == "2":
            vendor_menu(vendors)
        elif choice == "3":
            purchase_order_menu(products, vendors, purchase_orders)
        elif choice == "4":
            search_menu(products)
        elif choice == "5":
            sort_menu(products)
        elif choice == "6":
            reports_menu(products, purchase_orders)
        elif choice == "7":
            # Save all data before exiting.
            save_data(products, vendors, purchase_orders)
            print("\n  Thank you for using Moore Plants and Pots.")
            print("  Goodbye!\n")
            break
        else:
            print("  Invalid choice. Please enter a number from the menu.")

# Starts the program.
main()