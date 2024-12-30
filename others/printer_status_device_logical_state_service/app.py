from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_printer_status():
    response = {
        "crc": "0153C518",
        "dle_online": "yes",
        "no_paper": "no",
        "printer_error": "no"
    }
    return {
        "online": response.get("dle_online", "no"),
        "no_paper": response.get("no_paper", "yes"),
        "printer_error": response.get("printer_error", "yes")
    }

def get_device_logical_state():
    response = {
        "crc": "39B3018B",
        "enq_fiscal": "yes",
        "last_command_ok": "no",
        "in_transaction_mode": "no",
        "last_transaction_ok": "yes"
    }
    return {
        "fiscal_mode": response.get("enq_fiscal", "no"),
        "last_command_ok": response.get("last_command_ok", "no"),
        "transaction_mode": response.get("in_transaction_mode", "no"),
        "last_transaction_ok": response.get("last_transaction_ok", "no")
    }

@app.route('/printer/status', methods=['POST'])
def printer_status():
    try:
        data = request.get_json()
        if not data or 'packet' not in data:
            logging.warning("Invalid request received: missing 'packet' field.")
            return jsonify({"error": "Invalid request. 'packet' field is required."}), 400
        
        printer_status = get_printer_status()
        logging.info("Printer status retrieved successfully.")
        return jsonify(printer_status), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/device/logical-state', methods=['POST'])
def device_logical_state():
    try:
        data = request.get_json()
        if not data or 'packet' not in data:
            logging.warning("Invalid request received: missing 'packet' field.")
            return jsonify({"error": "Invalid request. 'packet' field is required."}), 400
        
        logical_state = get_device_logical_state()
        logging.info("Device logical state retrieved successfully.")
        return jsonify(logical_state), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.getenv("DEBUG_MODE", "True") == "True"
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug_mode, host=host, port=port)