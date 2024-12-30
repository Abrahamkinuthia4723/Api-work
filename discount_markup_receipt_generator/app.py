import xml.etree.ElementTree as ET


class Receipt:
    def __init__(self, cashier_name, system_number, cashbox_number):
        self.receipt = ET.Element('packet')
        self.begin_receipt = ET.SubElement(self.receipt, 'receipt', action="begin", mode="online")
        self.positions = []
        self.discounts = []
        self.payment = None
        self.close_receipt = ET.SubElement(self.receipt, 'receipt', action="close", system_number=system_number, 
                                           cashbox_number=cashbox_number, cashier=cashier_name)
    
    def add_position(self, name, quantity, price, rate, action="sale"):
        position = ET.SubElement(self.receipt, 'position', name=name, quantity=str(quantity), rate=rate, 
                                 price=str(price), action=action)
        self.positions.append(position)
    
    def add_discount(self, value, name, discount_id, action, rate=None):
        discount = ET.SubElement(self.receipt, 'discount', value=str(value), name=name, 
                                 discount_id=str(discount_id), action=action)
        if rate:
            discount.set('rate', rate)
        self.discounts.append(discount)
    
    def add_payment(self, payment_type, value):
        self.payment = ET.SubElement(self.receipt, 'payment', type=payment_type, action="add", value=str(value))
    
    def set_amount(self, amount):
        self.close_receipt.set('amount', str(amount))
    
    def get_xml(self):
        return ET.tostring(self.receipt, encoding='unicode', method='xml')


def generate_sale_with_quota_discount():
    receipt = Receipt(cashier_name="Adam Adam", system_number="123456", cashbox_number="02")
    receipt.add_position(name="water", quantity=1, price=11.00, rate="A")
    receipt.add_discount(value=10.00, name="special", discount_id=1, action="discount")
    receipt.add_position(name="soda water", quantity=1, price=5.00, rate="A")
    receipt.set_amount(6.00)  
    return receipt.get_xml()


def generate_sale_with_percentage_markup():
    receipt = Receipt(cashier_name="Adam Adam", system_number="123456", cashbox_number="02")
    receipt.add_position(name="water", quantity=1, price=11.00, rate="A")
    receipt.add_discount(value="10%", name="special", discount_id=1, action="markup")
    receipt.add_position(name="soda water", quantity=1, price=5.00, rate="A")
    receipt.set_amount(17.10) 
    return receipt.get_xml()


def generate_sale_with_percentage_discount():
    receipt = Receipt(cashier_name="Adam Adam", system_number="123456", cashbox_number="02")
    receipt.add_position(name="water", quantity=1, price=11.00, rate="A")
    receipt.add_position(name="soda water", quantity=1, price=5.00, rate="A")
    receipt.add_discount(value="20%", name="special", discount_id=1, action="discount")
    receipt.set_amount(16.00) 
    return receipt.get_xml()


def generate_sale_with_quota_markup_on_receipt():
    receipt = Receipt(cashier_name="Adam Adam", system_number="123456", cashbox_number="02")
    receipt.add_position(name="water", quantity=1, price=11.00, rate="A")
    receipt.add_position(name="soda water", quantity=1, price=5.00, rate="A")
    receipt.add_discount(value=5.00, name="special", discount_id=1, action="markup")
    receipt.set_amount(16.00)  
    return receipt.get_xml()


def generate_sale_with_position_subtotal_receipt_discounts():
    receipt = Receipt(cashier_name="Adam Adam", system_number="123456", cashbox_number="02")
    receipt.add_position(name="water", quantity=1, price=11.00, rate="A")
    receipt.add_discount(value=10.00, name="special", discount_id=1, action="discount")
    receipt.add_discount(value="10%", name="special", discount_id=1, action="discount")
    receipt.add_position(name="water", quantity=1, price=11.00, rate="A")
    receipt.add_discount(value="10%", name="special", discount_id=1, action="discount")
    receipt.add_discount(value=1.80, name="special", discount_id=1, action="discount")
    receipt.set_amount(9.00) 
    return receipt.get_xml()


def generate_percentage_discount_on_given_ptu_rate():
    receipt = Receipt(cashier_name="Adam Adam", system_number="123456", cashbox_number="02")
    positions = [
        ("coca cola", 1, 10.00, "A"),
        ("pepsi", 1, 20.00, "B"),
        ("fingersticks", 1, 30.00, "C"),
        ("kiwi", 1, 40.00, "D"),
        ("kiwi juice", 1, 10.00, "A"),
        ("water", 1, 20.00, "B"),
        ("mineral water", 1, 30.00, "C"),
        ("sugar", 1, 40.00, "D"),
        ("pepper", 1, 10.00, "A"),
        ("chili pepper", 1, 20.00, "B"),
        ("horseradish", 1, 30.00, "C"),
        ("tangerines", 1, 40.00, "D")
    ]
    for position in positions:
        receipt.add_position(name=position[0], quantity=position[1], price=position[2], rate=position[3])
    receipt.add_discount(value="20%", name="special", discount_id=1, action="discount", rate="A")
    receipt.add_payment(payment_type="cash", value=300.00)
    receipt.set_amount(294.00)  
    return receipt.get_xml()


def generate_quota_markup_on_goods_in_given_ptu_rate_c():
    receipt = Receipt(cashier_name="Adam Adam", system_number="123456", cashbox_number="02")
    positions = [
        ("coca cola", 1, 10.00, "A"),
        ("pepsi", 1, 20.00, "B"),
        ("fingersticks", 1, 30.00, "C"),
        ("kiwi", 1, 40.00, "D"),
        ("kiwi juice", 1, 10.00, "A"),
        ("water", 1, 20.00, "B"),
        ("mineral water", 1, 30.00, "C"),
        ("sugar", 1, 40.00, "D"),
        ("pepper", 1, 10.00, "A"),
        ("chili pepper", 1, 20.00, "B"),
        ("horseradish", 1, 30.00, "C"),
        ("tangerines", 1, 40.00, "D")
    ]
    for position in positions:
        receipt.add_position(name=position[0], quantity=position[1], price=position[2], rate=position[3])
    receipt.add_discount(value=10.00, name="special", discount_id=1, action="markup", rate="C")
    receipt.add_payment(payment_type="cash", value=340.00)
    receipt.set_amount(310.00)  
    return receipt.get_xml()


# Generate all receipts
receipts = {
    "sale_with_quota_discount": generate_sale_with_quota_discount(),
    "sale_with_percentage_markup": generate_sale_with_percentage_markup(),
    "sale_with_percentage_discount": generate_sale_with_percentage_discount(),
    "sale_with_quota_markup_on_receipt": generate_sale_with_quota_markup_on_receipt(),
    "sale_with_position_subtotal_receipt_discounts": generate_sale_with_position_subtotal_receipt_discounts(),
    "percentage_discount_on_given_ptu_rate": generate_percentage_discount_on_given_ptu_rate(),
    "quota_markup_on_goods_in_given_ptu_rate_c": generate_quota_markup_on_goods_in_given_ptu_rate_c()
}

# Print the generated receipts
for receipt_name, receipt_xml in receipts.items():
    print(f"--- {receipt_name} ---")
    print(receipt_xml)
    print("\n" + "-" * 80 + "\n")
