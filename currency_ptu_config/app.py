import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def validate_date_format(date):
    return bool(re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$', date))

def validate_exchange_rate(rate):
    try:
        value = float(rate)
        return 0.00000001 <= value <= 9999.99999999
    except ValueError:
        return False

@app.route('/currency', methods=['POST'])
def currency():
    try:
        data = request.data.decode('utf-8')
        root = ET.fromstring(data)

        if root.tag != 'packet':
            return jsonify(status="error", message="Invalid packet format."), 400

        currency_element = root.find('currency')
        if currency_element is None:
            return jsonify(status="error", message="Missing <currency> tag."), 400

        action = currency_element.get('action')
        if action == 'change':
            name = currency_element.get('name')
            date = currency_element.get('date')
            exchange_rate = currency_element.get('exchange_rate')

            if not (name and date and exchange_rate):
                return jsonify(status="error", message="Missing required attributes for 'change' action."), 400

            if not validate_date_format(date):
                return jsonify(status="error", message="Invalid date format. Use dd-mm-yyyy hh:mm."), 400

            if not validate_exchange_rate(exchange_rate):
                return jsonify(status="error", message="Exchange rate out of range. Valid range is 0.00000001 to 9999.99999999."), 400

            return jsonify(status="success", message=f"Currency changed to {name} successfully with an exchange rate of {exchange_rate}.")

        elif action == 'print':
            type_ = currency_element.get('type')
            name = currency_element.get('name')
            exchange_rate = currency_element.get('exchange_rate')

            if type_ == 'defined':
                if not (name and exchange_rate):
                    return jsonify(status="error", message="Missing 'name' or 'exchange_rate' for 'defined' type."), 400

                if not validate_exchange_rate(exchange_rate):
                    return jsonify(status="error", message="Exchange rate out of range. Valid range is 0.00000001 to 9999.99999999."), 400

                return jsonify(status="success", message=f"Printing mode set to 'defined' for {name} with an exchange rate of {exchange_rate}.")

            elif type_ == 'none':
                return jsonify(status="success", message="Printing mode set to 'none' (without currency conversion).")

            else:
                return jsonify(status="error", message="Invalid type for 'print' action."), 400

        else:
            return jsonify(status="error", message="Invalid action."), 400

    except ET.ParseError:
        return jsonify(status="error", message="Invalid XML format."), 400

@app.route('/tax_rates', methods=['POST'])
def tax_rates():
    try:
        data = request.data.decode('utf-8')
        root = ET.fromstring(data)

        if root.tag != 'packet':
            return jsonify(status="error", message="Invalid packet format."), 400

        tax_rates_element = root.find('tax_rates')
        if tax_rates_element is None:
            return jsonify(status="error", message="Missing <tax_rates> tag."), 400

        action = tax_rates_element.get('action')
        if action == 'set':
            checkbox = tax_rates_element.get('checkbox')
            cashier = tax_rates_element.get('cashier')
            date = tax_rates_element.get('date')

            if date and not validate_date_format(date):
                return jsonify(status="error", message="Invalid date format. Use dd-mm-yyyy hh:mm."), 400

            ptu_elements = tax_rates_element.findall('ptu')
            if not ptu_elements:
                return jsonify(status="error", message="No PTU rates provided."), 400

            ptu_rates = []
            for ptu in ptu_elements:
                name = ptu.get('name')
                value = ptu.text
                if not (name and value):
                    return jsonify(status="error", message="Missing name or value in PTU rates."), 400

                ptu_rates.append(f"{name} = {value}")

            return jsonify(status="success", message=f"Tax rates set successfully: {', '.join(ptu_rates)}.")

        elif action == 'get':
            # Example: 
            tax_rates_response = ET.Element('packet')
            rates = ET.SubElement(tax_rates_response, 'tax_rates')

            ptu_a = ET.SubElement(rates, 'ptu', name="A")
            ptu_a.text = "23%"

            ptu_b = ET.SubElement(rates, 'ptu', name="B")
            ptu_b.text = "free"

            return ET.tostring(tax_rates_response, encoding='unicode'), 200

        else:
            return jsonify(status="error", message="Invalid action."), 400

    except ET.ParseError:
        return jsonify(status="error", message="Invalid XML format."), 400

if __name__ == '__main__':
    app.run(debug=True)
