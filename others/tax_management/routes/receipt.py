from flask import Blueprint, request, jsonify
from models.data_store import RECEIPT_DATA, QR_DATA

receipt_bp = Blueprint('receipt', __name__)

@receipt_bp.route('/start', methods=['POST'])
def start_receipt():
    data = request.get_json()
    receipt_data = RECEIPT_DATA.get("start")
    receipt_data.update(data)
    return jsonify(receipt_data), 200

@receipt_bp.route('/info', methods=['POST'])
def receipt_info():
    data = request.get_json()
    receipt_number = data.get('receipt_number', 1)
    qr_info = QR_DATA.get(receipt_number, {})
    return jsonify(qr_info), 200
