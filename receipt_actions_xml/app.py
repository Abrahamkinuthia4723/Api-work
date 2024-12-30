import xml.etree.ElementTree as ET

def create_receipt_with_storno():
    # Begin receipt
    packet = ET.Element("packet")
    receipt = ET.SubElement(packet, "receipt", action="begin", mode="online")
    
    # Add positions
    position1 = ET.SubElement(packet, "position", name="bread", quantity="1", rate="A", price="1.00", action="sale")
    position2 = ET.SubElement(packet, "position", name="juice", quantity="1", rate="A", price="1.00", action="sale")
    position3 = ET.SubElement(packet, "position", name="beer", quantity="1", rate="A", price="2.00", action="sale")
    
    # Storno action for juice
    position_storno = ET.SubElement(packet, "position", name="juice", quantity="1", rate="A", price="1.00", action="storno")
    
    # Close receipt
    receipt_close = ET.SubElement(packet, "receipt", action="close", system_number="123456", cashbox_number="02", cashier="Adam Adam", amount="2.00")
    
    return ET.tostring(packet, encoding="unicode")

def create_receipt_with_footer_lines():
    packet = ET.Element("packet")
    receipt = ET.SubElement(packet, "receipt", action="begin", mode="online")
    
    # Add positions
    position1 = ET.SubElement(packet, "position", name="bread1", quantity="1", rate="A", price="1.00", action="sale")
    
    # Add footer lines
    non_fiscal_line = ET.SubElement(packet, "non-fiscal_line", type="definition")
    line1 = ET.SubElement(non_fiscal_line, "line")
    line1.text = "line 1"
    line2 = ET.SubElement(non_fiscal_line, "line")
    line2.text = "line 2"
    line3 = ET.SubElement(non_fiscal_line, "line")
    line3.text = "@line3"
    
    # Close receipt
    receipt_close = ET.SubElement(packet, "receipt", action="close", system_number="123456", cashbox_number="02", cashier="Adam Adam", amount="1.00")
    
    return ET.tostring(packet, encoding="unicode")

def create_in_advance_payment():
    packet = ET.Element("packet")
    receipt = ET.SubElement(packet, "receipt", action="begin", mode="online")
    
    # Add in advance payment
    in_advance = ET.SubElement(packet, "in_advance", action="in advance", rate="A", description="Television set", value="100")
    
    # Close receipt
    receipt_close = ET.SubElement(packet, "receipt", action="close", system_number="123456", cashbox_number="02", cashier="Adam Adam", amount="100.00")
    
    return ET.tostring(packet, encoding="unicode")

def create_in_advance_payment_storno():
    packet = ET.Element("packet")
    receipt = ET.SubElement(packet, "receipt", action="begin", mode="online")
    
    # In-advance payment and storno
    in_advance = ET.SubElement(packet, "in_advance", action="in advance", rate="A", description="Television set", value="100")
    in_advance_storno = ET.SubElement(packet, "in_advance", action="in advance_storno", rate="A", description="Television set", value="100")
    
    # Add a sale position
    position = ET.SubElement(packet, "position", name="bread", quantity="1", rate="A", price="1.00", action="sale")
    
    # Close receipt
    receipt_close = ET.SubElement(packet, "receipt", action="close", system_number="123456", cashbox_number="02", cashier="Adam Adam", amount="1.00")
    
    return ET.tostring(packet, encoding="unicode")

def create_settlement_in_advance():
    packet = ET.Element("packet")
    receipt = ET.SubElement(packet, "receipt", action="begin", mode="online")
    
    # Sale position
    position = ET.SubElement(packet, "position", name="Television set", quantity="1", rate="A", price="500.00", action="sale")
    
    # In-advance settlement
    in_advance = ET.SubElement(packet, "in_advance", action="in advance_settlement", rate="A", description="Television set", value="100", surcharge="400")
    
    # Close receipt
    receipt_close = ET.SubElement(packet, "receipt", action="close", system_number="123", cashbox_number="1", cashier="Jan Kowalski", amount="400.00")
    
    return ET.tostring(packet, encoding="unicode")

def create_reversal_in_advance_settlement():
    packet = ET.Element("packet")
    receipt = ET.SubElement(packet, "receipt", action="begin", mode="online")
    
    # Sale position
    position = ET.SubElement(packet, "position", name="Television set", quantity="1", rate="A", price="500.00", action="sale")
    
    # In-advance settlement and reversal
    in_advance = ET.SubElement(packet, "in_advance", action="in advance_settlement", rate="A", description="Television set", value="100")
    in_advance_storno = ET.SubElement(packet, "in_advance", action="storno_in advance_settlement", rate="A", description="Television set", value="100")
    
    # Close receipt
    receipt_close = ET.SubElement(packet, "receipt", action="close", system_number="123", cashbox_number="1", cashier="Jan Kowalski", amount="500.00")
    
    return ET.tostring(packet, encoding="unicode")

# Test the functions
print(create_receipt_with_storno())
print(create_receipt_with_footer_lines())
print(create_in_advance_payment())
print(create_in_advance_payment_storno())
print(create_settlement_in_advance())
print(create_reversal_in_advance_settlement())
