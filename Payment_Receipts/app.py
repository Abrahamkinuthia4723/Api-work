import xml.etree.ElementTree as ET

class Receipt:
    def __init__(self, cashier, system_number, cashbox_number, amount, receipt_mode="online"):
        self.receipt = ET.Element("packet")
        self.add_receipt_begin(receipt_mode)
        self.items = []
        self.payments = []
        self.discounts = []
        self.cashier = cashier
        self.system_number = system_number
        self.cashbox_number = cashbox_number
        self.amount = amount

    def add_receipt_begin(self, mode):
        receipt = ET.SubElement(self.receipt, "receipt", action="begin", mode=mode)
    
    def add_item(self, name, quantity, unit, price, action, rate='A', plu='', description=''):
        item = ET.SubElement(self.receipt, "position", name=name, quantity=str(quantity), unit=unit, rate=rate, price=str(price), recipe="", charge="", plu=plu, description=description, action=action)
        self.items.append(item)

    def add_discount(self, value, discount_id, action):
        discount = ET.SubElement(self.receipt, "discount", value=value, discount_id=str(discount_id), action=action)
        self.discounts.append(discount)
    
    def add_payment(self, payment_type, action, value, name=''):
        payment = ET.SubElement(self.receipt, "payment", type=payment_type, action=action, value=str(value), name=name)
        self.payments.append(payment)

    def add_receipt_close(self):
        receipt_close = ET.SubElement(self.receipt, "receipt", action="close", system_number=self.system_number, cashbox_number=str(self.cashbox_number), cashier=self.cashier, amount=str(self.amount))
        for discount in self.discounts:
            self.receipt.append(discount)
    
    def generate_xml(self):
        self.add_receipt_close()
        return ET.tostring(self.receipt, encoding='unicode', method='xml')

# Function to simulate different receipt scenarios
def generate_receipt_scenarios():
    scenarios = []

    # Receipt with many items
    receipt_1 = Receipt(cashier="Jan Kowalski", system_number="123", cashbox_number="1", amount="655.00")
    receipt_1.add_item("water", 1, "pcs", 100.00, "sale", plu="#")
    receipt_1.add_item("juice", 1, "pcs", 150.00, "sale")
    receipt_1.add_item("sugar", 1, "pcs", 50.00, "storno", plu="@")
    receipt_1.add_item("bread", 1, "pcs", 50.00, "sale")
    receipt_1.add_discount("10%", 2, "discount")
    receipt_1.add_item("butter", 1, "pcs", 50.00, "sale", plu="#")
    receipt_1.add_item("eggs", 1, "pcs", 50.00, "sale")
    receipt_1.add_item("beer", 1, "pcs", 50.00, "sale")
    receipt_1.add_discount("10.00", 6, "markup")
    receipt_1.add_item("candy", 1, "pcs", 50.00, "sale")
    receipt_1.add_item("fingersticks", 1, "pcs", 50.00, "sale")
    receipt_1.add_item("bananas", 1, "pcs", 50.00, "sale")
    receipt_1.add_item("nuts", 1, "pcs", 50.00, "sale")
    receipt_1.add_payment("card", "add", 20.00, "card")
    receipt_1.add_payment("cheque", "add", 30.00, "cheque")
    receipt_1.add_payment("credit", "add", 50.00, "credit")
    receipt_1.add_payment("mobil", "add", 100.00, "mobil")
    scenarios.append(receipt_1.generate_xml())

    # Goods sale
    receipt_2 = Receipt(cashier="Adam Adam", system_number="02", cashbox_number="02", amount="1.00")
    receipt_2.add_item("bread", 1, "pcs", 1.00, "sale")
    scenarios.append(receipt_2.generate_xml())

    # Payment with change
    receipt_3 = Receipt(cashier="Adam Adam", system_number="02", cashbox_number="02", amount="1.00")
    receipt_3.add_item("bread", 1, "pcs", 1.00, "sale")
    receipt_3.add_payment("cash", "add", 10.00)
    scenarios.append(receipt_3.generate_xml())

    # Payment by card
    receipt_4 = Receipt(cashier="Adam Adam", system_number="02", cashbox_number="02", amount="1.00")
    receipt_4.add_item("bread", 1, "pcs", 1.00, "sale")
    receipt_4.add_payment("card", "add", 1.00, "VISA")
    scenarios.append(receipt_4.generate_xml())

    # Payment by card with change
    receipt_5 = Receipt(cashier="Adam Adam", system_number="02", cashbox_number="02", amount="1.00")
    receipt_5.add_item("bread", 1, "pcs", 1.00, "sale")
    receipt_5.add_payment("card", "add", 10.00, "VISA")
    scenarios.append(receipt_5.generate_xml())

    # Supporting forms of payment – many forms of payment
    receipt_6 = Receipt(cashier="Adam Adam", system_number="123456", cashbox_number="02", amount="300.00")
    receipt_6.add_item("coca cola", 1, "pcs", 10.00, "sale")
    receipt_6.add_item("pepsi", 1, "pcs", 20.00, "sale")
    receipt_6.add_item("fingersticks", 1, "pcs", 30.00, "sale")
    receipt_6.add_item("kiwi", 1, "pcs", 40.00, "sale")
    receipt_6.add_item("kiwi juice", 1, "pcs", 10.00, "sale")
    receipt_6.add_item("water", 1, "pcs", 20.00, "sale")
    receipt_6.add_item("mineral water", 1, "pcs", 30.00, "sale")
    receipt_6.add_item("sugar", 1, "pcs", 40.00, "sale")
    receipt_6.add_item("pepper", 1, "pcs", 10.00, "sale")
    receipt_6.add_item("chili pepper", 1, "pcs", 20.00, "sale")
    receipt_6.add_item("horseradish", 1, "pcs", 30.00, "sale")
    receipt_6.add_item("tangerines", 1, "pcs", 40.00, "sale")
    receipt_6.add_payment("card", "add", 20.00, "card")
    receipt_6.add_payment("cheque", "add", 30.00, "cheque")
    receipt_6.add_payment("credit", "add", 50.00, "credit")
    receipt_6.add_payment("mobil", "add", 100.00, "mobil")
    scenarios.append(receipt_6.generate_xml())

    # Supporting forms of payment – cancelling 3 from 4 payments
    receipt_7 = Receipt(cashier="Adam Adam", system_number="123456", cashbox_number="02", amount="300.00")
    receipt_7.add_item("coca cola", 1, "pcs", 10.00, "sale")
    receipt_7.add_item("pepsi", 1, "pcs", 20.00, "sale")
    receipt_7.add_item("fingersticks", 1, "pcs", 30.00, "sale")
    receipt_7.add_item("kiwi", 1, "pcs", 40.00, "sale")
    receipt_7.add_item("kiwi juice", 1, "pcs", 10.00, "sale")
    receipt_7.add_item("water", 1, "pcs", 20.00, "sale")
    receipt_7.add_item("mineral water", 1, "pcs", 30.00, "sale")
    receipt_7.add_item("sugar", 1, "pcs", 40.00, "sale")
    receipt_7.add_item("pepper", 1, "pcs", 10.00, "sale")
    receipt_7.add_item("chili pepper", 1, "pcs", 20.00, "sale")
    receipt_7.add_item("horseradish", 1, "pcs", 30.00, "sale")
    receipt_7.add_item("tangerines", 1, "pcs", 40.00, "sale")
    receipt_7.add_payment("card", "add", 20.00, "card")
    receipt_7.add_payment("cheque", "add", 30.00, "cheque")
    receipt_7.add_payment("credit", "add", 50.00, "credit")
    receipt_7.add_payment("mobil", "add", 100.00, "mobil")
    receipt_7.add_payment("card", "delete", 20.00, "card")
    receipt_7.add_payment("cheque", "delete", 30.00, "cheque")
    receipt_7.add_payment("credit", "delete", 50.00, "credit")
    scenarios.append(receipt_7.generate_xml())

    return scenarios

receipt_scenarios = generate_receipt_scenarios()
for idx, receipt_xml in enumerate(receipt_scenarios):
    print(f"Receipt {idx + 1}:")
    print(receipt_xml)
    print("\n" + "-"*80 + "\n")
