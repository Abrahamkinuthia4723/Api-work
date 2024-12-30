from flask import Flask, request, jsonify

app = Flask(__name__)

mock_receipts = {
    "1": {
        "middleware_invoice_number": "0100099410000000001",
        "qr_code_link": "https://tims-test.kra.go.ke/KRA-Portal/invoiceChk.htm?actionCode=loadPage&invoiceNo=",
        "trader_sys_number": "1",
        "trader_sys_number_EX": "123/236"
    },
    "last": {
        "middleware_invoice_number": "0100099410000000001",
        "qr_code_link": "https://tims-test.kra.go.ke/KRA-Portal/invoiceChk.htm?actionCode=loadPage&invoiceNo=",
        "trader_sys_number": "1",
        "trader_sys_number_EX": "123/236"
    }
}

@app.route('/receipt/info', methods=['POST'])
def get_receipt_info():
    try:
        data = request.get_json()

        action = data.get('info', {}).get('action')
        receipt_number = data.get('info', {}).get('receipt_number')
        trader_sys_number_EX = data.get('info', {}).get('trader_sys_number_EX')

        response_data = {
            "action": action
        }

        if action == "receipt" and receipt_number:
            receipt_info = mock_receipts.get(str(receipt_number))
            if receipt_info:
                response_data.update(receipt_info)
                return jsonify(response_data), 200
            else:
                return jsonify({"error": "Receipt not found"}), 404
        
        elif action == "receipt" and trader_sys_number_EX:
            for key, value in mock_receipts.items():
                if value["trader_sys_number_EX"] == trader_sys_number_EX:
                    response_data.update(value)
                    return jsonify(response_data), 200
            return jsonify({"error": "No matching receipt found for trader_sys_number_EX"}), 404
        
        elif action == "last_receipt":
            last_receipt_info = mock_receipts.get("last")
            if last_receipt_info:
                response_data.update(last_receipt_info)
                return jsonify(response_data), 200
            else:
                return jsonify({"error": "Last receipt not found"}), 404

        else:
            return jsonify({"error": "Invalid action or parameters"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
