from flask import Blueprint, request, jsonify
from .services import force_transfer, get_sent_receipts

teams_server_bp = Blueprint('teams_server', __name__)

@teams_server_bp.route('/force_transfer', methods=['POST'])
def force_transfer_route():
    data = request.get_json()
    response = force_transfer(data)
    return jsonify(response)

@teams_server_bp.route('/get_receipts', methods=['POST'])
def get_sent_receipts_route():
    data = request.get_json()
    response = get_sent_receipts(data)
    return jsonify(response)
