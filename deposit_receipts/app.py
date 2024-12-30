import xml.etree.ElementTree as ET
from typing import List


def create_receipt(action: str, mode: str = "online", system_number: str = "123456", 
                   cashbox_number: str = "02", cashier: str = "Adam Adam", 
                   amount: float = 0.00) -> ET.Element:
    receipt = ET.Element("receipt", action=action, mode=mode)
    if action == "close":
        receipt.set("system_number", system_number)
        receipt.set("cashbox_number", cashbox_number)
        receipt.set("cashier", cashier)
        receipt.set("amount", str(amount))
    return receipt


def create_position(name: str, quantity: int, rate: str, price: float, 
                    action: str = "sale") -> ET.Element:
    position = ET.Element("position", name=name, quantity=str(quantity), unit="", 
                          rate=rate, price=str(price), recipe="", charge="", 
                          plu="", description="", action=action)
    return position


def create_deposit(action: str, price: float, type_: str, quantity: int) -> ET.Element:
    deposit = ET.Element("deposit", action=action, price=str(price), 
                         type=type_, quantity=str(quantity))
    return deposit


def create_payment(action: str, value: float, payment_type: str = "cash") -> ET.Element:
    payment = ET.Element("payment", action=action, type=payment_type, value=str(value))
    return payment


def create_receipt_with_deposit_return() -> ET.Element:
    packet = ET.Element("packet")
    receipt = create_receipt(action="begin")
    packet.append(receipt)
    packet.append(create_position(name="soda water", quantity=1, rate="A", price=5.00))
    packet.append(create_deposit(action="sale", price=0.40, type_="returned", quantity=2))
    packet.append(create_receipt(action="close", amount=5.00))
    return packet


def create_receipt_with_deposit_reversal() -> ET.Element:
    packet = ET.Element("packet")
    receipt = create_receipt(action="begin")
    packet.append(receipt)
    packet.append(create_position(name="soda water", quantity=1, rate="A", price=5.00))
    packet.append(create_deposit(action="storno", price=0.35, type_="returned", quantity=1))
    packet.append(create_receipt(action="close", amount=5.00))
    return packet


def create_receipt_with_deposit_collections_and_refunds() -> ET.Element:
    packet = ET.Element("packet")
    receipt = create_receipt(action="begin")
    packet.append(receipt)
    packet.append(create_position(name="soda water", quantity=1, rate="A", price=5.00))
    packet.append(create_deposit(action="sale", price=0.35, type_="taken", quantity=2))
    packet.append(create_deposit(action="sale", price=0.10, type_="returned", quantity=8))
    packet.append(create_deposit(action="sale", price=0.40, type_="returned", quantity=2))
    packet.append(create_payment(action="add", value=5.00))
    packet.append(create_receipt(action="close", amount=5.00))
    return packet


def generate_xml_string(packet: ET.Element) -> str:
    return ET.tostring(packet, encoding="unicode", method="xml")


def prettify_xml(xml_string: str) -> str:
    """Pretty print the XML string to make it more readable."""
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_string)
    return dom.toprettyxml(indent="  ")


def generate_all_receipts():
    receipts: List[ET.Element] = [
        create_receipt_with_deposit_return(),
        create_receipt_with_deposit_reversal(),
        create_receipt_with_deposit_collections_and_refunds()
    ]
    
    for index, receipt in enumerate(receipts):
        xml_string = generate_xml_string(receipt)
        pretty_xml = prettify_xml(xml_string)
        
        with open(f"receipt_{index + 1}.xml", "w") as file:
            file.write(pretty_xml)


if __name__ == "__main__":
    generate_all_receipts()
