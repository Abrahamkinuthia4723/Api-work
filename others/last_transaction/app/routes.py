from flask import Blueprint, request, jsonify
from app.data import LAST_TRANSACTION

main = Blueprint("main", __name__)

@main.route('/last_transaction', methods=['POST'])
def last_transaction_info():
    """
    API Endpoint to query the status of the last transaction.
    """
    try:
        data = request.get_json()
        action = data.get("info", {}).get("action")

        if action != "lasttransaction":
            return jsonify({"error": f"Invalid action: {action}. Expected 'lasttransaction'."}), 400

        return jsonify(LAST_TRANSACTION), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
