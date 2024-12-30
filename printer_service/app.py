from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = {
    "fiscalisation": {},
    "producer_data": {},
    "service_lock": None,
    "logs": {
        "update_logs": [],
        "module_logs": []
    },
    "service_reviews": []
}

@app.route('/fiscalisation', methods=['POST'])
def fiscalisation():
    try:
        packet = request.json['fiscalisation']
        action = packet['action']
        if action in ['training_mode', 'fiscalization']:
            data_store['fiscalisation'] = {
                "action": action,
                "type_device": packet['type_device'],
                "nip": packet['nip'],
                "office_name": packet['office_name'],
                "service_name": packet['service_name'],
                "service_man_name": packet['service_man_name'],
                "service_id": packet['service_id'],
                "tax_office_code": packet['tax_office_code'],
                "reg_number": packet['reg_number'],
                "tax_service": packet['tax_service'],
                "type_numbering": packet['type_numbering']
            }
            return jsonify({"message": "Fiscalisation data processed successfully"}), 200
        return jsonify({"error": "Invalid action"}), 400
    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/producer', methods=['POST'])
def producer_data():
    try:
        packet = request.json['producer']
        data_store['producer_data'] = {
            "unique_no": packet['unique_no'],
            "producer_no": packet['producer_no'],
            "mac": packet['mac'],
            "producer_option": packet['producer_option']
        }
        return jsonify({"message": "Producer data set successfully"}), 200
    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/service', methods=['POST'])
def service():
    try:
        packet = request.json['service']
        action = packet['action']
        if action == 'lock':
            data_store['service_lock'] = {
                "date": packet.get('date'),
                "description": packet.get('description'),
                "password": packet.get('password')
            }
            return jsonify({"message": "Service locked successfully"}), 200
        elif action == 'unlock':
            data_store['service_lock'] = None
            return jsonify({"message": "Service unlocked successfully"}), 200
        elif action == 'review':
            data_store['service_reviews'].append({
                "date": packet['date'],
                "description": packet.get('description')
            })
            return jsonify({"message": "Service review set successfully"}), 200
        elif action == 'review_done':
            return jsonify({"message": "Service review confirmed"}), 200
        return jsonify({"error": "Invalid action"}), 400
    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logs/update', methods=['POST'])
def update_logs():
    try:
        packet = request.json['updatelog']
        action = packet['action']
        if action == 'begin':
            data_store['logs']['update_logs'].append("Log data start")
            return jsonify({"message": "Update log download started"}), 200
        elif action == 'next':
            return jsonify({"message": "Next update log chunk"}), 200
        return jsonify({"error": "Invalid action"}), 400
    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logs/module', methods=['POST'])
def module_logs():
    try:
        packet = request.json['processlog']
        action = packet['action']
        if action == 'begin':
            logs = data_store['logs']['module_logs']
            filtered_logs = [log for log in logs if log_matches(packet, log)]
            return jsonify({"logs": filtered_logs}), 200
        elif action == 'next':
            return jsonify({"message": "Next module log chunk"}), 200
        return jsonify({"error": "Invalid action"}), 400
    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/report', methods=['POST'])
def service_review_report():
    try:
        packet = request.json['report']
        if packet['type'] == 'service_review':
            return jsonify({"reviews": data_store['service_reviews']}), 200
        return jsonify({"error": "Invalid report type"}), 400
    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def log_matches(packet, log):
    start = packet.get('date_time_start')
    stop = packet.get('date_time_stop')
    level = packet.get('level')
    module = packet.get('module')
    if start and log['date_time'] < start:
        return False
    if stop and log['date_time'] > stop:
        return False
    if level and log['level'] != level:
        return False
    if module and log['module'] != module:
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True)
