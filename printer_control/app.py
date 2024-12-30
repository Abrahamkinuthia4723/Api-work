from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/info/port', methods=['POST'])
def get_port_info():
    try:
        data = request.get_json()
        if not data or 'packet' not in data:
            logging.warning("Invalid request: missing 'packet' field.")
            return jsonify({"error": "Invalid request. 'packet' field is required."}), 400

        if data['packet'].get('action') == "port":
            response = {
                "info": {
                    "action": "port",
                    "value": "PC1"
                }
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid action."}), 400
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/info/repository', methods=['POST'])
def get_repository_info():
    try:
        data = request.get_json()
        if not data or 'packet' not in data:
            logging.warning("Invalid request: missing 'packet' field.")
            return jsonify({"error": "Invalid request. 'packet' field is required."}), 400

        if data['packet'].get('action') == "repository":
            response = {
                "info": {
                    "action": "repository",
                    "date_send": "20-06-2018",
                    "date_send_correct": "20-06-2018",
                    "jpk_send_count": 14,
                    "jpk_actual_send_no": 1
                }
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid action."}), 400
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/control/<action>', methods=['POST'])
def control_action(action):
    try:
        data = request.get_json()
        if not data or 'packet' not in data:
            logging.warning("Invalid request: missing 'packet' field.")
            return jsonify({"error": "Invalid request. 'packet' field is required."}), 400

        if action == "beep":
            response = {"control": {"action": "beep", "status": "success"}}
        elif action == "paper_feed":
            value = data['packet'].get('value', 1)
            cutter = data['packet'].get('cutter', "no")
            response = {
                "control": {
                    "action": "paper_feed",
                    "value": value,
                    "cutter": cutter,
                    "status": "success"
                }
            }
        elif action == "drawer":
            response = {"control": {"action": "drawer", "status": "drawer_opened"}}
        elif action == "display":
            display_lines = {k: v for k, v in data['packet'].items() if k.startswith("line_")}
            response = {"control": {"action": "display", "lines": display_lines, "status": "success"}}
        elif action == "display_external":
            text = data['packet'].get('text', "")
            response = {"control": {"action": "display_external", "text": text, "status": "success"}}
        elif action == "clear_display":
            response = {"control": {"action": "clear_display", "status": "display_cleared"}}
        elif action == "menu_open":
            response = {"control": {"action": "menu_open", "status": "menu_opened"}}
        else:
            return jsonify({"error": "Unsupported action."}), 400

        logging.info(f"Action '{action}' executed successfully.")
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.getenv("DEBUG_MODE", "True") == "True"
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug_mode, host=host, port=port)
