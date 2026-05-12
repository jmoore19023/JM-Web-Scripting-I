# =============================================================================
# models.py
#
# Moore Plants and Pots - Inventory and Purchase Order System
# Created by: John Moore
# Created on: 2024-05-11
#
# PURPOSE:
# Started with model file due to every other part of this program hinging off it. 
# The data, classes, and objects built from this file will drive and create the basis for the remaining parts of the program.
# Here I define the data models for the program. There are three main models: Product, Vendor, and PurchaseOrder. 
# Each model has its own specific structures and will store the both the information and methods to display/convert that data.
# With a solid model foundation, we can build the rest of the program around them, making the rest of the program more robust and easier to maintain/troubleshoot.
# =============================================================================


class Product: 

    # Product class created to represent a single product. This class is the corenerstone to creating product objects and storing product information in inventory.
    # Class contains methods to display product information and convert the product object to a dictionary for  storage and retrieval from JSON files.
    # The Product class includes several attributes which are listed in the __init__ code section below. 

    def __init__(self, product_id, name, category, quantity, reorder_level,
                 reorder_quantity, price, vendor_id, active=True,
                 clearance_date=None, clearance_price=None):

        self.product_id = product_id          # Unique ID, e.g. "P001"
        self.name = name                      # Product name, e.g. "Tomato Seeds"
        self.category = category              # Category, e.g. "Seeds"
        self.quantity = quantity              # How many we currently have in stock
        self.reorder_level = reorder_level    # If stock drops to this number, reorder
        self.reorder_quantity = reorder_quantity  # How many to order when restocking
        self.price = price                    # Selling price per unit
        self.vendor_id = vendor_id            # Links this product to a vendor
        self.active = active                  # True = sold here, False = discontinued
        self.clearance_date = clearance_date  # Date to start selling at reduced price
        self.clearance_price = clearance_price  # Reduced price during clearance

    def display(self):

        # Simple display function that prints summary of a product. 
        # Added a condition to check if product is on clearance for items that are past their clearance date
        # display() prints a readable summary of this product to the screen.
      
        if self.active == True: #Conditional statement assigning active/discontinued status of product.
            status = "Active"
        else:
            status = "Discontinued"


        print(f"  Product ID    : {self.product_id}")
        print(f"  Name          : {self.name}")
        print(f"  Category      : {self.category}")
        print(f"  Quantity      : {self.quantity}")
        print(f"  Reorder Level : {self.reorder_level}")
        print(f"  Reorder Qty   : {self.reorder_quantity}")
        print(f"  Price         : ${self.price:.2f}")
        print(f"  Vendor ID     : {self.vendor_id}")
        print(f"  Status        : {status}")

        if self.clearance_date: #Prints if item is on clearance with discounted price and clearance date.
            print(f"  Clearance Date: {self.clearance_date}")
            print(f"  Clearance Price: ${self.clearance_price:.2f}")


    def to_dict(self):

        # to dict() is a method used to convert product objects into a dictionary format. 
        # Necessary for saviing products to a JSON file and returns the values as key:value pairs.

        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "reorder_level": self.reorder_level,
            "reorder_quantity": self.reorder_quantity,
            "price": self.price,
            "vendor_id": self.vendor_id,
            "active": self.active,
            "clearance_date": self.clearance_date,
            "clearance_price": self.clearance_price
        }

    @classmethod
    def from_dict(cls, data):

        
        # Class method that creates a product from a dictionary. Opposite of to_dict() method.
        # Method used to convert data from JSON file into product object that can be used in the program.

        return cls(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            quantity=data["quantity"],
            reorder_level=data["reorder_level"],
            reorder_quantity=data["reorder_quantity"],
            price=data["price"],
            vendor_id=data["vendor_id"],
            active=data.get("active", True),
            clearance_date=data.get("clearance_date", None),
            clearance_price=data.get("clearance_price", None)
        )


class Vendor:

    # Vendor class created to represent suppliers for the business and is responsible for both creating vendor objects and storing vendor contact/business information..
    # Class contains methods to display vendor information and convert the vendor object to a dictionary for storage and retrieval from JSON files.
    # Vendors are linked to products through the vendor_id field, essentially actings as a primary key and allowing any product to be traced back to its supplier.

    def __init__(self, vendor_id, name, contact_name, phone, email, address):

        self.vendor_id = vendor_id        # Unique ID, e.g. "V001"
        self.name = name                  # Business name, e.g. "Green Thumb Wholesale"
        self.contact_name = contact_name  # Person we contact at this vendor
        self.phone = phone                # Their phone number
        self.email = email                # Their email address
        self.address = address            # Their city/state or full address

    def display(self):
        print(f"  Vendor ID    : {self.vendor_id}")
        print(f"  Name         : {self.name}")
        print(f"  Contact      : {self.contact_name}")
        print(f"  Phone        : {self.phone}")
        print(f"  Email        : {self.email}")
        print(f"  Address      : {self.address}")

    def to_dict(self):
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            vendor_id=data["vendor_id"],
            name=data["name"],
            contact_name=data["contact_name"],
            phone=data["phone"],
            email=data["email"],
            address=data["address"]
        )


class PurchaseOrder:


    # PurchaseOrder class created to represent an order placed with vendors to restock products.
    # Class is different from others due to representing a transaction/event versus an actual object such as a product or vendor. 
    # PurchaseOrder class is signficant with it tying the product and vendor classes together and representing the process of restocking inventory.
    # This class uses a list of dictionaries to represent multiple items versus a single object due to the inherent nature of a PO having multiple products to one order.

    def __init__(self, po_number, vendor_id, date_created, items,
                 total_cost, status="Open"):

        #Status attribute provides visiblity to whether an order is open or has been received.

        self.po_number = po_number        # Unique PO number, e.g. "PO001"
        self.vendor_id = vendor_id        # Which vendor this order goes to
        self.date_created = date_created  # Date the order was created (string)
        self.items = items                # List of items ordered (see above)
        self.total_cost = total_cost      # Total dollar amount of this order
        self.status = status              # "Open" or "Received"

    def display(self):
        print(f"  PO Number    : {self.po_number}")
        print(f"  Vendor ID    : {self.vendor_id}")
        print(f"  Date Created : {self.date_created}")
        print(f"  Status       : {self.status}")
        print(f"  Total Cost   : ${self.total_cost:.2f}")
        print(f"  Items Ordered:")

        # For loop used to iterate through all items in the purchase order list with possibility of multiple items per order.
        for item in self.items:
            print(f"    - {item['product_name']} "
                  f"(ID: {item['product_id']}) "
                  f"x{item['quantity']} "
                  f"@ ${item['unit_price']:.2f} each")

    # to_dict() and from_dict() used for same reason as other classes. converts this purchase order to a dictionary for saving.

    def to_dict(self):
        return {
            "po_number": self.po_number,
            "vendor_id": self.vendor_id,
            "date_created": self.date_created,
            "items": self.items,
            "total_cost": self.total_cost,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            po_number=data["po_number"],
            vendor_id=data["vendor_id"],
            date_created=data["date_created"],
            items=data["items"],
            total_cost=data["total_cost"],
            status=data.get("status", "Open")
        )