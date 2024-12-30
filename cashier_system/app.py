from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = {
    "cashier": None,
    "cash_balance": 0.0,
    "last_error": None,
    "goods": [
        {"name": "item1", "ptu": "A"},
        {"name": "item2", "ptu": "B"}
    ]
}

@app.route('/cashier', methods=['POST'])
def cashier():
    try:
        packet = request.json
        action = packet['cashier']['action']

        if action == 'login':
            data_store['cashier'] = {
                "name": packet['cashier'].get('name', None),
                "number": packet['cashier'].get('number', None)
            }
            return jsonify({
                "message": "Cashier logged in successfully",
                "cashier": data_store['cashier']
            }), 200

        elif action == 'logoff':
            if data_store['cashier'] is None:
                return jsonify({"error": "No cashier is currently logged in"}), 404

            data_store['cashier'] = None
            return jsonify({"message": "Cashier logged off successfully"}), 200

        elif action == 'state':
            if data_store['cashier'] is None:
                return jsonify({"message": "No cashier is currently logged in"}), 404

            return jsonify({"cashier": data_store['cashier']}), 200

        else:
            return jsonify({"error": "Invalid action"}), 400

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/cash', methods=['POST'])
def cash():
    try:
        packet = request.json
        action = packet['cash']['action']

        if action == 'payin':
            value = float(packet['cash']['value'])
            data_store['cash_balance'] += value
            return jsonify({"message": "Pay-in successful", "new_balance": data_store['cash_balance']}), 200

        elif action == 'payout':
            value = float(packet['cash']['value'])
            if value > data_store['cash_balance']:
                return jsonify({"error": "Insufficient funds"}), 400

            data_store['cash_balance'] -= value
            return jsonify({"message": "Pay-out successful", "new_balance": data_store['cash_balance']}), 200

        elif action == 'read':
            return jsonify({"cash_balance": data_store['cash_balance']}), 200

        else:
            return jsonify({"error": "Invalid action"}), 400

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/error', methods=['POST'])
def error():
    try:
        packet = request.json
        action = packet['error']['action']

        if action == 'set':
            value = packet['error'].get('value', 'display')
            data_store['last_error'] = value
            return jsonify({"message": f"Error mode set to {value}"}), 200

        elif action == 'get':
            return jsonify({"last_error": data_store['last_error']}), 200

        else:
            return jsonify({"error": "Invalid action"}), 400

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/dbcheck', methods=['POST'])
def dbcheck():
    try:
        packet = request.json
        action = packet['dbcheck']['action']

        if action == 'begin':
            mode = packet['dbcheck'].get('mode', 'all')
            return jsonify({"message": f"Goods report started in {mode} mode"}), 200

        elif action == 'check':
            plu_name = packet['dbcheck'].get('plu_name', None)
            if plu_name:
                matching_goods = [good for good in data_store['goods'] if good['name'] == plu_name]
            else:
                matching_goods = data_store['goods']

            return jsonify({"matching_goods": matching_goods}), 200

        elif action == 'end':
            return jsonify({"message": "Goods report ended"}), 200

        else:
            return jsonify({"error": "Invalid action"}), 400

    except KeyError:
        return jsonify({"error": "Invalid packet structure"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
