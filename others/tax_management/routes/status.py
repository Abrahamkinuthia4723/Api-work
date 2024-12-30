from flask import Blueprint, jsonify
from models.data_store import STATUS_DATA

status_bp = Blueprint('status', __name__)

@status_bp.route('/checkout', methods=['POST'])
def get_status():
    return jsonify(STATUS_DATA), 200
