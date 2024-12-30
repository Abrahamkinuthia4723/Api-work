from flask import Flask, request, jsonify, Response
import xml.etree.ElementTree as ET
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/create_receipt_item', methods=['POST'])
def create_receipt_item():
    try:
        data = request.get_json()
        required_fields = ['name', 'quantity', 'quantityunit', 'ptu', 'price', 'total', 'action']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        name = data['name']
        quantity = data['quantity']
        quantityunit = data['quantityunit']
        ptu = data['ptu']
        price = data['price']
        total = data['total']
        action = data['action']
        hscode_index = data.get('hscode_index', '')
        plu = data.get('plu', '')
        description = data.get('description', '')

        item = ET.Element("item")
        item.set("name", name)
        item.set("quantity", str(quantity))
        item.set("quantityunit", quantityunit)
        item.set("ptu", ptu)
        item.set("price", str(price))
        item.set("total", str(total))
        item.set("action", action)
        item.set("hscode_index", hscode_index)
        item.set("plu", plu)
        item.set("description", description)

        packet = ET.Element("packet")
        packet.append(item)

        xml_str = ET.tostring(packet, encoding='unicode', method='xml')

        return Response(xml_str, mimetype='application/xml')

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
