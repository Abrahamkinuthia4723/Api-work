from flask import Blueprint, request, jsonify
from models.data_store import SERVER_DATA

server_bp = Blueprint('server', __name__)

@server_bp.route('/force_transfer', methods=['POST'])
def force_transfer():
    return jsonify({"message": "Server force transfer initiated"}), 200

@server_bp.route('/get_files', methods=['POST'])
def get_files():
    return jsonify(SERVER_DATA), 200
