# Cash register information.

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

CASH_REGISTER_INFO = {
    "checkout": {
        "receipt": {
            "lasterror": "0",
            "isfiscal": "yes",
            "receiptopen": "no",
            "lastreceipterror": "no",
            "resetcount": "0",
            "date": "08-10-2013",
            "receiptcount": "11",
            "cash": "444.76",
            "uniqueno": "ABC12345678",
            "lastreceipt": "11",
            "lastinvoice": "1",
            "lastprintout": "47",
            "cycles": "1130909187",
            "seconds": "180",
            "begin_date": "2000-00-00 00:00:00",
            "receipt_count_in_report": "1",
            "ptu": {
                "A": "12.50",
                "B": "0.00",
                "C": "0.00",
                "D": "0.00",
                "G": "0.00"
            }
        },
        "invoice": {
            "lasterror": "0",
            "isfiscal": "yes",
            "receiptopen": "no",
            "lastreceipterror": "no",
            "resetcount": "0",
            "date": "08-10-2013",
            "receiptcount": "5",
            "cash": "1000.00",
            "uniqueno": "DEF98765432",
            "lastreceipt": "5",
            "lastinvoice": "3",
            "lastprintout": "22",
            "cycles": "1130909187",
            "seconds": "300",
            "begin_date": "2000-01-01 00:00:00",
            "receipt_count_in_report": "2",
            "ptu": {
                "A": "15.00",
                "B": "0.00",
                "C": "0.00",
                "D": "0.00",
                "G": "0.00"
            }
        }
    },
    "uptime": {
        "uptime_seconds": 86400,
        "uptime_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

@app.route('/cash_register', methods=['POST'])
def cash_register_info():
    try:
        data = request.get_json()
        action = data.get("info", {}).get("action")
        type_ = data.get("info", {}).get("type", "receipt")

        if action not in CASH_REGISTER_INFO:
            return jsonify({"error": f"Invalid action: {action}. Valid actions are: checkout, uptime."}), 400

        if action == "checkout":
            if type_ not in CASH_REGISTER_INFO[action]:
                return jsonify({"error": f"Invalid type: {type_}. Valid types are: receipt, invoice."}), 400
            response_data = CASH_REGISTER_INFO[action][type_]
            return jsonify(response_data), 200

        if action == "uptime":
            uptime_data = CASH_REGISTER_INFO[action]
            return jsonify(uptime_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
