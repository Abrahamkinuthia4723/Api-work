#from additional commnds.docx

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Receipt, Report, PrinterData
from utils import parse_xml_to_dict, validate_date_range

app = Flask(__name__)
CORS(app)

VALID_FORMATS = ['nonfiscalprintout', 'standard', 'to_pc']
VALID_KINDS = ['receipt', 'reserved', 'dailyreport', 'nonfiscal', 'all', 'receipt_by_trad_sys_num']

@app.route('/receipt', methods=['POST'])
def get_receipt_info():
    data = request.get_json()
    
    if 'receipt_number' in data['info']:
        receipt_number = data['info']['receipt_number']
        receipt = Receipt.get_receipt_by_number(receipt_number)
        return jsonify(receipt), 200
    
    if 'trader_sys_number_EX' in data['info']:
        trader_sys_number = data['info']['trader_sys_number_EX']
        receipt = Receipt.get_receipt_by_trader_sys_number(trader_sys_number)
        return jsonify(receipt), 200

    return jsonify({"error": "Invalid request"}), 400

@app.route('/last_receipt', methods=['POST'])
def get_last_signed_receipt():
    data = request.get_json()
    
    if data['info']['action'] == 'last_receipt':
        receipt = Receipt.get_last_signed_receipt()
        return jsonify(receipt), 200
    
    return jsonify({"error": "Invalid action"}), 400

@app.route('/printer_data', methods=['POST'])
def printer_data():
    data = request.get_json()

    if 'trader_sys_number_EX' in data['info']:
        trader_sys_number = data['info']['trader_sys_number_EX']
        printer_data = PrinterData.get_data_by_trader_sys_number(trader_sys_number)
        return jsonify(printer_data), 200

    return jsonify({"error": "Trader system number not provided"}), 400

@app.route('/report', methods=['POST'])
def generate_report():
    data = request.get_json()

    if 'report' in data:
        report_data = data['report']
        trader_sys_number = report_data.get('trader_sys_number_EX')
        kind = report_data.get('kind')
        format = report_data.get('format', 'nonfiscalprintout')
        from_date = report_data.get('from')
        to_date = report_data.get('to')

        if kind not in VALID_KINDS:
            return jsonify({"error": f"Invalid kind. Valid kinds are: {', '.join(VALID_KINDS)}"}), 400
        
        if format not in VALID_FORMATS:
            return jsonify({"error": f"Invalid format. Valid formats are: {', '.join(VALID_FORMATS)}"}), 400

        if from_date and to_date:
            from_date, to_date = validate_date_range(from_date, to_date)

        if kind == 'receipt_by_trad_sys_num':
            if not trader_sys_number:
                return jsonify({"error": "Trader system number is required for 'receipt_by_trad_sys_num'"}), 400
            report = Report.generate_report_by_trader_sys_number(trader_sys_number)
        else:
            report = Report.generate_report_by_kind(kind, from_date, to_date, format)

        return jsonify(report), 200

    return jsonify({"error": "Invalid report request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
