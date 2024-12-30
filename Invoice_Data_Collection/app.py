import xml.etree.ElementTree as ET

def create_invoice_packet(invoice_data, positions, payments=None, discounts=None, non_fiscal_lines=None):
    packet = ET.Element("packet")
    
    # Create the invoice element with provided attributes
    invoice = ET.SubElement(packet, "invoice", action="begin", 
                            number=invoice_data['number'], 
                            nip=invoice_data['nip'], 
                            description=invoice_data['description'], 
                            payment_name=invoice_data['payment_name'], 
                            payment_data=invoice_data['payment_data'],
                            receiver=invoice_data.get('receiver', ""),
                            issuer=invoice_data.get('issuer', ""),
                            copy_number=str(invoice_data['copy_number']), 
                            margines=invoice_data['margines'],
                            options_buyer_name=invoice_data['options_buyer_name'],
                            options_seller_name=invoice_data['options_seller_name'],
                            space_for_signature=invoice_data['space_for_signature'],
                            paid=invoice_data.get('paid', ""),
                            sale_date=invoice_data['sale_date'])
    
    # Add customer information
    for customer in invoice_data.get('customers', []):
        ET.SubElement(invoice, "customer").text = customer
    
    # Add options (if any)
    for option_id in invoice_data.get('options', []):
        ET.SubElement(invoice, "option", id=str(option_id))

    # Add positions
    for position in positions:
        position_element = ET.SubElement(packet, "position", 
                                         name=position['name'], 
                                         quantity=str(position['quantity']), 
                                         unit=position['unit'], 
                                         rate=position['rate'], 
                                         price=str(position['price']), 
                                         recipe=position.get('recipe', ""),
                                         charge=position.get('charge', ""),
                                         plu=position.get('plu', ""),
                                         description=position.get('description', ""),
                                         action=position['action'])
    
    # Add payments (if any)
    if payments:
        for payment in payments:
            ET.SubElement(packet, "payment", type=payment['type'], 
                          name=payment['name'], action=payment['action'], 
                          value=str(payment['value']))

    # Add discounts (if any)
    if discounts:
        for discount in discounts:
            ET.SubElement(packet, "discount", value=str(discount['value']), 
                          name=discount['name'], discount_id=str(discount['discount_id']), 
                          action=discount['action'])

    # Add non-fiscal lines (if any)
    if non_fiscal_lines:
        for line in non_fiscal_lines:
            ET.SubElement(packet, "non-fiscal_line", type=line['type'], 
                          id=str(line['id']), value=str(line['value']))
    
    # Add invoice close action
    ET.SubElement(packet, "invoice", action="close", 
                  buyer=invoice_data['buyer'], 
                  amount=str(invoice_data['amount']), 
                  system_number=invoice_data['system_number'], 
                  cashbox_number=invoice_data['cashbox_number'], 
                  cashier=invoice_data['cashier'])

    return ET.tostring(packet, encoding="unicode", method="xml")


# Example usage:

invoice_data = {
    'number': '120/2012',
    'nip': '1234567890',
    'description': 'both',
    'payment_name': 'cash',
    'payment_data': '10-10-2013',
    'copy_number': 255,
    'margines': 'no',
    'options_buyer_name': 'information',
    'options_seller_name': 'no',
    'space_for_signature': 'yes',
    'sale_date': '10-10-2013',
    'customers': ['receiver data 1'],
    'options': [1, 2, 11],
    'buyer': 'jan jan',
    'amount': 15.00,
    'system_number': '123',
    'cashbox_number': '02',
    'cashier': 'Adam Adam'
}

positions = [
    {'name': 'fruit juice', 'quantity': 2, 'unit': 'pcs', 'rate': 'A', 'price': 2.00, 'action': 'sale'},
    {'name': 'beer no alcoh.', 'quantity': 1, 'unit': 'pcs', 'rate': 'A', 'price': 1.00, 'action': 'sale'},
    {'name': 'soda water', 'quantity': 1, 'unit': 'pcs', 'rate': 'A', 'price': 1.00, 'action': 'sale'}
]

payments = [
    {'type': 'card', 'name': 'VISA', 'action': 'add', 'value': 5.00},
    {'type': 'cheque', 'name': 'cheque', 'action': 'add', 'value': 5.00},
    {'type': 'credit', 'name': 'credit', 'action': 'add', 'value': 5.00},
    {'type': 'transfer', 'name': 'transfer', 'action': 'add', 'value': 5.00}
]

discounts = [
    {'value': 10.00, 'name': 'SPECIAL', 'discount_id': 1, 'action': 'markup'}
]

non_fiscal_lines = [
    {'type': 'definition', 'id': 1, 'value': 'abc line 1'},
    {'type': 'definition', 'id': 2, 'value': 'abc line 2'},
    {'type': 'definition', 'id': 3, 'value': 'abc line 3'}
]

# Generate XML invoice
invoice_xml = create_invoice_packet(invoice_data, positions, payments, discounts, non_fiscal_lines)
print(invoice_xml)
