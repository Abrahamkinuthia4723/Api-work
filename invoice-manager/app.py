import datetime
from typing import Optional, List

class Invoice:
    def __init__(self, invoice_type: str, number: Optional[str] = None, nip: Optional[str] = '',
                 description: Optional[str] = 'both', payment_name: Optional[str] = 'cash',
                 payment_date: Optional[str] = None, recipient: Optional[str] = '',
                 issuer: Optional[str] = '', copies: int = 1, margins: Optional[str] = 'no',
                 signature_area: Optional[str] = 'yes', customer_name_options: Optional[str] = 'all',
                 seller_name_options: Optional[str] = 'all', paidlabel: Optional[str] = '',
                 sell_date: Optional[str] = None, additional_info: Optional[str] = '', options: Optional[List[int]] = None):
        self.invoice_type = invoice_type
        self.number = number
        self.nip = nip
        self.description = description
        self.payment_name = payment_name
        self.payment_date = payment_date if payment_date else datetime.date.today().strftime("%d-%m-%Y")
        self.recipient = recipient
        self.issuer = issuer
        self.copies = copies
        self.margins = margins
        self.signature_area = signature_area
        self.customer_name_options = customer_name_options
        self.seller_name_options = seller_name_options
        self.paidlabel = paidlabel
        self.sell_date = sell_date if sell_date else self.payment_date
        self.additional_info = additional_info
        self.options = options if options else []

    def to_xml(self) -> str:
        options_str = ''.join([f'<option id="{opt}" />' for opt in self.options])
        return f'''<packet>
<invoice action="begin" number="{self.number}" nip="{self.nip}" description="{self.description}" 
payment_name="{self.payment_name}" payment_date="{self.payment_date}" recipient="{self.recipient}" 
issuer="{self.issuer}" copies="{self.copies}" margins="{self.margins}" signature_area="{self.signature_area}"
customer_name_options="{self.customer_name_options}" seller_name_options="{self.seller_name_options}" 
paidlabel="{self.paidlabel}" sell_date="{self.sell_date}">
{options_str}
<customer>{self.additional_info}</customer>
</invoice>
</packet>'''

class InvoiceCancellation:
    @staticmethod
    def cancel_invoice() -> str:
        return '''<packet>
<invoice action="cancel"></invoice>
</packet>'''

class InvoiceClosure:
    def __init__(self, buyer: str, total: float, system_no: str, checkbox_no: int, cashier: str):
        self.buyer = buyer
        self.total = total
        self.system_no = system_no
        self.checkbox_no = checkbox_no
        self.cashier = cashier

    def to_xml(self) -> str:
        return f'''<packet>
<invoice action="close" buyer="{self.buyer}" total="{self.total}" system_no="{self.system_no}" 
checkbox_no="{self.checkbox_no}" cashier="{self.cashier}"></invoice>
</packet>'''

class Discount:
    def __init__(self, value: str, name: str, descid: Optional[int] = 1, action: Optional[str] = 'discount'):
        self.value = value
        self.name = name
        self.descid = descid
        self.action = action

    def to_xml(self) -> str:
        return f'''<packet>
<discount value="{self.value}" name="{self.name}" descid="{self.descid}" action="{self.action}">
</discount>
</packet>'''

class NonFiscalLine:
    def __init__(self, type: str = 'line', id: int = 1, value: float = 0.0):
        self.type = type
        self.id = id
        self.value = value

    def to_xml(self) -> str:
        return f'''<packet>
<non-fiscal_line type="{self.type}" id="{self.id}" value="{self.value}"></non-fiscal_line>
</packet>'''

class FooterDefinition:
    def __init__(self, lines: List[str]):
        self.lines = lines

    def to_xml(self) -> str:
        lines_str = ''.join([f'<line>{line}</line>' for line in self.lines])
        return f'''<packet>
<non-fiscal_line type="definition">
{lines_str}
</non-fiscal_line>
</packet>'''

# Example usage

invoice = Invoice(invoice_type='invoice', number='120/2012', payment_date='10-10-2013', sell_date='10-10-2013', 
                  customer_name_options='all', seller_name_options='all', options=[1, 3, 9])
print("Invoice XML:\n", invoice.to_xml())

cancellation = InvoiceCancellation()
print("\nCancel Invoice XML:\n", cancellation.cancel_invoice())

closure = InvoiceClosure(buyer='Jan Jan', total=123.32, system_no='123', checkbox_no=1, cashier='Jan')
print("\nClose Invoice XML:\n", closure.to_xml())

discount = Discount(value="23%", name="Occasional", descid=1)
print("\nDiscount XML:\n", discount.to_xml())

non_fiscal_line = NonFiscalLine(type="line", id=1, value=1234.56)
print("\nNon-Fiscal Line XML:\n", non_fiscal_line.to_xml())

footer = FooterDefinition(lines=["abc line 1", "abc line 2", "abc line 3"])
print("\nFooter Definition XML:\n", footer.to_xml())
