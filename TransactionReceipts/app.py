import xml.etree.ElementTree as ET
from datetime import datetime

class ReceiptPrinter:
    def __init__(self):
        self.receipt_opened = False
        self.receipt_data = {}
        self.transaction_type = "receipt"
        self.transaction_mode = "online"
        self.net_total = 233
        self.gross_total = 343
        self.tax_details = {
            'A': {'tax': 23, 'net': 100, 'gross': 123}
        }

    def create_xml(self, root_element):
        """Helper function to generate XML string from ElementTree"""
        return ET.tostring(root_element, encoding="unicode")

    def open_receipt(self, mode="online", pharmaceutical="no"):
        """Opens a receipt with specified mode and pharmaceutical status."""
        if self.receipt_opened:
            raise Exception("Receipt already opened.")
        
        receipt = ET.Element("receipt")
        receipt.set("action", "begin")
        receipt.set("mode", mode)
        receipt.set("pharmaceutical", pharmaceutical)

        self.receipt_data = {
            "action": "begin",
            "mode": mode,
            "pharmaceutical": pharmaceutical
        }
        
        self.receipt_opened = True
        print("Receipt opened:", ET.tostring(receipt, encoding='unicode'))
    
    def cancel_receipt(self):
        """Cancels the current receipt."""
        if not self.receipt_opened:
            raise Exception("No receipt opened to cancel.")
        
        receipt = ET.Element("receipt")
        receipt.set("action", "cancel")
        
        self.receipt_opened = False
        self.receipt_data = {}
        print("Receipt cancelled:", ET.tostring(receipt, encoding='unicode'))
    
    def close_receipt(self, system_no, checkbox_no=None, cashier=None, total=None, charge=None, nip=None):
        """Closes the current receipt with the specified details."""
        if not self.receipt_opened:
            raise Exception("No receipt opened to close.")
        
        receipt = ET.Element("receipt")
        receipt.set("action", "close")
        receipt.set("system_no", system_no)
        
        if checkbox_no:
            receipt.set("checkbox_no", str(checkbox_no))
        if cashier:
            receipt.set("cashier", cashier)
        if total:
            receipt.set("total", str(total))
        if charge:
            receipt.set("charge", str(charge))
        if nip:
            receipt.set("nip", nip)
        
        self.receipt_opened = False
        self.receipt_data = {}
        print("Receipt closed:", ET.tostring(receipt, encoding='unicode'))

    def add_item_to_receipt(self, name, quantity, quantity_unit, ptu, price, total, recipe="", charge="", plu="", description="", action="sale"):
        """Adds an item to the receipt."""
        item = ET.Element("item")
        item.set("name", name)
        item.set("quantity", str(quantity))
        item.set("quantity_unit", quantity_unit)
        item.set("ptu", ptu)
        item.set("price", str(price))
        item.set("total", str(total))
        item.set("recipe", recipe)
        item.set("charge", charge)
        item.set("plu", plu)
        item.set("description", description)
        item.set("action", action)
        
        print("Item added to receipt:", ET.tostring(item, encoding='unicode'))

    def apply_discount_or_markup(self, value, name=None, desc_id=None, type="subtotal", total=None, ptu="A", action="discount"):
        """Applies a discount or markup to the receipt."""
        discount = ET.Element("discount")
        discount.set("value", value)
        discount.set("name", name if name else "")
        discount.set("desc_id", str(desc_id) if desc_id else "")
        discount.set("type", type)
        discount.set("total", str(total) if total else "")
        discount.set("ptu", ptu)
        discount.set("action", action)
        
        print("Discount/Markup applied:", ET.tostring(discount, encoding='unicode'))

    def settlement_of_returnable_packages(self, action, price, package_type="taken", quantity=1):
        """Handles the settlement of returnable packages."""
        container = ET.Element("container")
        container.set("action", action)
        container.set("price", str(price))
        container.set("type", package_type)
        container.set("quantity", str(quantity))
        
        print("Settlement of returnable packages:", ET.tostring(container, encoding='unicode'))

    def get_transaction_state(self):
        """Returns current transaction state including net/gross totals and type"""
        info = ET.Element("info")
        info.set("action", "transaction")
        info.set("net_total", str(self.net_total))
        info.set("gross_total", str(self.gross_total))
        info.set("type", self.transaction_type)
        info.set("mode", self.transaction_mode)

        # Add total tax details
        for name, details in self.tax_details.items():
            total = ET.SubElement(info, "total")
            total.set("name", name)
            total.set("tax", str(details['tax']))
            total.set("net", str(details['net']))
            total.set("gross", str(details['gross']))

        return self.create_xml(info)

    def get_device_info(self, action="date"):
        """Gets information about the device (either date or version)."""
        info = ET.Element("info")
        info.set("action", action)
        
        if action == "date":
            info.set("date", datetime.now().strftime("%d-%m-%Y %H:%M"))
        elif action == "version":
            info.set("version", "1.0.0") 

        print("Device Info:", ET.tostring(info, encoding='unicode'))

# Example usage:
printer = ReceiptPrinter()

# 1. Open receipt
printer.open_receipt(mode="online", pharmaceutical="no")

# 2. Add item to receipt
printer.add_item_to_receipt(name="item1", quantity=2, quantity_unit="pcs", ptu="A", price=10.00, total=20.00)

# 3. Apply discount
printer.apply_discount_or_markup(value="10%", name="Seasonal Discount", action="discount")

# 4. Settlement of returnable packages (sale)
printer.settlement_of_returnable_packages(action="sale", price=1.00, package_type="taken", quantity=1)

# 5. Get transaction state
transaction_state = printer.get_transaction_state()
print("Transaction State:")
print(transaction_state)

# 6. Get device info (date)
printer.get_device_info(action="date")

# 7. Close receipt
printer.close_receipt(system_no="1234", cashier="John", total=50.00, charge=0.00)
