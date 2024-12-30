import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def parse_xml_data(data):
    """Helper function to parse XML data and handle errors."""
    try:
        root = ET.fromstring(data)
        if root.tag != 'packet':
            raise ValueError("Invalid packet format.")
        return root
    except ET.ParseError:
        raise ValueError("Invalid XML format.")
    except ValueError as e:
        raise e

def error_response(message, status=400):
    """Helper function to generate error responses."""
    return jsonify(status="error", message=message), status

def handle_missing_attribute(element, *attributes):
    """Check if all required attributes are present in an element."""
    missing = [attr for attr in attributes if not element.get(attr)]
    if missing:
        return f"Missing attributes: {', '.join(missing)}."
    return None

@app.route('/fiscal_memory', methods=['POST'])
def fiscal_memory():
    try:
        root = parse_xml_data(request.data.decode('utf-8'))
        fiscal_memory_element = root.find('fiscal_memory')
        if not fiscal_memory_element:
            return error_response("Missing <fiscal_memory> tag.")

        action = fiscal_memory_element.get('action')
        if action not in ['get', 'next']:
            return error_response("Invalid action.")

        if action == 'get':
            from_time = fiscal_memory_element.get('from')
            if not from_time:
                return error_response("Missing 'from' attribute for action 'get'.")
            
            # Return the first record (for demonstration purposes)
            return jsonify(
                status="success",
                message="Returning first record",
                data={
                    "type": "report",
                    "time": "01-01-2024 12:00",
                    "receipt_count": 23,
                    "invoice_count": 3,
                    "canceled_receipt_count": 2,
                    "number": 1,
                    "last_receipt": 4,
                    "last_invoice": 2,
                    "sale": "12342.33",
                    "tax": "20",
                    "total_sale": "123213.12",
                    "total_tax": "232.12",
                    "invoice_sale": "21.33",
                    "invoice_tax": "22.12",
                    "invoice_total_sale": "1213.52",
                    "invoice_total_tax": "3231.12",
                    "currency_name": "PLN",
                    "non_taxable": "0.00",
                    "tickets": "0",
                    "normal": "0",
                    "subsidy": "0",
                    "reduced": "0",
                    "abroad": "0",
                    "ptu": [
                        {
                            "name": "A",
                            "rate": "23%",
                            "sale": "2.31",
                            "tax": "23.12",
                            "total_tax": "21142.23",
                            "invoice_sale": "2.20",
                            "invoice_tax": "0.23",
                            "invoice_total_tax": "232.12"
                        }
                    ]
                }
            )

        elif action == 'next':
            return jsonify(
                status="success",
                message="Returning next record",
                data={
                    "type": "report",
                    "time": "01-01-2024 13:00",
                    "receipt_count": 24,
                    "invoice_count": 4,
                    "canceled_receipt_count": 1,
                    "number": 2,
                    "last_receipt": 5,
                    "last_invoice": 3,
                    "sale": "10000.00",
                    "tax": "15",
                    "total_sale": "150000.00",
                    "total_tax": "3000.00",
                    "invoice_sale": "25.00",
                    "invoice_tax": "2.50",
                    "invoice_total_sale": "250.00",
                    "invoice_total_tax": "50.00",
                    "currency_name": "PLN",
                    "non_taxable": "0.00",
                    "tickets": "5",
                    "normal": "5",
                    "subsidy": "0",
                    "reduced": "0",
                    "abroad": "0",
                    "ptu": [
                        {
                            "name": "B",
                            "rate": "5%",
                            "sale": "1.50",
                            "tax": "5.00",
                            "total_tax": "15.00",
                            "invoice_sale": "0.50",
                            "invoice_tax": "0.05",
                            "invoice_total_tax": "0.10"
                        }
                    ]
                }
            )

        type_ = fiscal_memory_element.get('type')
        if type_ == 'reset':
            reason = fiscal_memory_element.get('reason')
            if not reason:
                return error_response("Missing reason for reset.")
            return jsonify(status="success", message=f"Memory reset due to {reason}.")
        
        elif type_ == 'tax_rates':
            ptu_elements = fiscal_memory_element.findall('ptu')
            if not ptu_elements:
                return error_response("Missing PTU rates in 'tax_rates' type.")
            
            # Example response for tax rates
            tax_rates_response = {
                "type": "tax_rates",
                "time": "01-01-2024 12:00",
                "ptu": [
                    {"name": "A", "rate": "23%"},
                    {"name": "B", "rate": "free"}
                ]
            }
            return jsonify(status="success", message="Tax rates programmed.", data=tax_rates_response)

        elif type_ == 'currency_set' or type_ == 'currency_change':
            name = fiscal_memory_element.get('name')
            change_time = fiscal_memory_element.get('change_time')
            exchange_rate = fiscal_memory_element.get('exchange_rate')
            if not (name and change_time and exchange_rate):
                return error_response("Missing attributes for currency set/change.")
            return jsonify(
                status="success", 
                message=f"Currency {type_} to {name} with exchange rate {exchange_rate} effective from {change_time}."
            )

        elif type_ == 'card_close':
            number = fiscal_memory_element.get('number')
            close_time = fiscal_memory_element.get('close_time')
            if not (number and close_time):
                return error_response("Missing attributes for card close.")
            return jsonify(
                status="success",
                message=f"Card number {number} closed at {close_time}."
            )

        elif type_ == 'end':
            return jsonify(status="success", message="End of data reached.")

        else:
            return error_response("Invalid or unsupported type.")

    except ValueError as e:
        return error_response(str(e))

if __name__ == '__main__':
    app.run(debug=True)
