#Downloading data from the protected memory by the trader system number

import random
from flask import Flask, request, jsonify
from utils import create_response_json, validate_date

app = Flask(__name__)

VALID_FORMATS = ['nonfiscalprintout', 'standard', 'to_pc']
VALID_KINDS = ['receipt', 'invoice', 'dailyreport', 'nonfiscal', 'all', 'receipt_by_trad_sys_num']

@app.route('/download_data', methods=['POST'])
def download_data():
    try:
        data = request.get_json()
        report = data.get('packet', {}).get('report', {})
        
        from_date = report.get('from')
        to_date = report.get('to')
        kind = report.get('kind')
        format = report.get('format', 'to_pc')
        action = report.get('action')
        trader_sys_number = report.get('trader_sys_number_EX')
        nip = report.get('nip', '')

        if format not in VALID_FORMATS:
            return jsonify({"error": f"Invalid format. Valid formats are: {', '.join(VALID_FORMATS)}"}), 400
        
        if kind not in VALID_KINDS:
            return jsonify({"error": f"Invalid kind. Valid kinds are: {', '.join(VALID_KINDS)}"}), 400

        if from_date and to_date:
            from_date = validate_date(from_date)
            to_date = validate_date(to_date)

        if action == 'begin':
            receipt_number = random.randint(1, 100)
        elif action == 'next':
            receipt_number = random.randint(1, 100)
        else:
            return jsonify({"error": "Invalid action"}), 400

        if kind == 'receipt_by_trad_sys_num':
            if not trader_sys_number:
                return jsonify({"error": "Missing trader_sys_number_EX for 'receipt_by_trad_sys_num'"}), 400
            receipt_number = random.randint(1, 100)

        response_json = create_response_json(from_date, to_date, kind, format, action, receipt_number)

        if receipt_number == 0:
            response_json = {"message": "No more receipts available."}

        return jsonify(response_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
