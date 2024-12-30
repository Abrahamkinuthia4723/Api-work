from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/receipt/open', methods=['POST'])
def open_receipt():
    try:
        data = request.get_json()

        action = data.get('receipt', {}).get('action')
        mode = data.get('receipt', {}).get('mode', 'online')  
        pharmaceutical = data.get('receipt', {}).get('pharmaceutical', 'no')  
        receipt_type = data.get('receipt', {}).get('type', 'tax_invoice') 
        relevant_receipt_number = data.get('receipt', {}).get('relevant_receipt_number', '0')
        nip = data.get('receipt', {}).get('nip')
        exemption_number = data.get('receipt', {}).get('exemption_number')
        selldate = data.get('receipt', {}).get('selldate')
        trader_sys_number = data.get('receipt', {}).get('trader_sys_number')
        trader_sys_number_ex = data.get('receipt', {}).get('trader_sys_number_EX')

        if not nip:
            return jsonify({"error": "NIP (PIN) is required."}), 400

        if mode not in ['online', 'offline']:
            return jsonify({"error": "Invalid mode. Must be 'online' or 'offline'."}), 400
        if pharmaceutical not in ['yes', 'no']:
            return jsonify({"error": "Invalid pharmaceutical value. Must be 'yes' or 'no'."}), 400
        if receipt_type not in ['tax_invoice', 'credit_note_item', 'credit_note_all', 'debit_note']:
            return jsonify({"error": "Invalid type. Must be 'tax_invoice', 'credit_note_item', 'credit_note_all', or 'debit_note'."}), 400

        response_data = {
            "action": action,
            "status": "Receipt opened successfully",
            "mode": mode,
            "pharmaceutical": pharmaceutical,
            "type": receipt_type,
            "relevant_receipt_number": relevant_receipt_number,
            "nip": nip,
            "exemption_number": exemption_number,
            "selldate": selldate,
            "trader_sys_number": trader_sys_number,
            "trader_sys_number_ex": trader_sys_number_ex,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
