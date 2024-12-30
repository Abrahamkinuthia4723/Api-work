from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database for storing configurations and states
data_store = {
    "usb_config": {},
    "config": {},
    "current_time": None,
    "header": []
}

# USB configuration
@app.route('/usb', methods=['POST'])
def usb_configuration():
    try:
        packet = request.json
        action = packet['usb']['action']

        if action == 'set':
            data_store['usb_config'] = {
                "usb_modem_pid": packet['usb'].get('usb_modem_pid'),
                "usb_modem_vid": packet['usb'].get('usb_modem_vid'),
                "usb_modem_type": packet['usb'].get('usb_modem_type'),
                "usb_modem_protocol": packet['usb'].get('usb_modem_protocol'),
                "usb_modem_interface": packet['usb'].get('usb_modem_interface'),
                "usb_ex_pid": packet['usb'].get('usb_ex_pid'),
                "usb_ex_vid": packet['usb'].get('usb_ex_vid'),
                "usb_ex_type": packet['usb'].get('usb_ex_type'),
                "usb_ex_protocol": packet['usb'].get('usb_ex_protocol'),
                "usb_ex_interface": packet['usb'].get('usb_ex_interface')
            }
            return jsonify({"message": "USB configuration set successfully", "usb_config": data_store['usb_config']}), 200

        elif action == 'get':
            return jsonify({"usb_config": data_store['usb_config']}), 200

        else:
            return jsonify({"error": "Invalid action"}), 400

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Configuration 
@app.route('/config', methods=['POST'])
def configuration():
    try:
        packet = request.json
        action = packet['config']['action']

        if action == 'set':
            for item in packet['config']['set']:
                data_store['config'][item['id']] = item['value']
            return jsonify({"message": "Configuration parameters set successfully", "config": data_store['config']}), 200

        elif action == 'get':
            from_id = int(packet['config'].get('from', 0))
            to_id = int(packet['config'].get('to', 0))
            filtered_config = {key: value for key, value in data_store['config'].items() if from_id <= int(key) <= to_id}
            return jsonify({"config": filtered_config}), 200

        else:
            return jsonify({"error": "Invalid action"}), 400

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Clock setting 
@app.route('/clock', methods=['POST'])
def clock():
    try:
        packet = request.json
        data_store['current_time'] = packet['clock']['date']
        return jsonify({"message": "Date and time set successfully", "current_time": data_store['current_time']}), 200

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Header programming
@app.route('/header', methods=['POST'])
def header():
    try:
        packet = request.json
        action = packet['header_online']['action']

        if action == 'set':
            data_store['header'] = packet['header_online']['line']
            return jsonify({"message": "Header set successfully", "header": data_store['header']}), 200

        elif action == 'get':
            return jsonify({"header": data_store['header']}), 200

        else:
            return jsonify({"error": "Invalid action"}), 400

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
