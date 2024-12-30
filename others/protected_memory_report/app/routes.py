from flask import Blueprint, request, jsonify
from .validations import validate_report_request

report_bp = Blueprint('report', __name__)

@report_bp.route('/', methods=['POST'])
def generate_report():
    """Handles the report generation request."""
    data = request.get_json()

    is_valid, errors = validate_report_request(data)
    if not is_valid:
        return jsonify({"error": errors}), 400

    report = data.get('report', {})
    report_type = report.get("type")
    kind = report.get("kind")
    format_ = report.get("format", "nonfiscalprintout")
    trader_sys_number_EX = report.get("trader_sys_number_EX")
    from_date = report.get("from")
    to_date = report.get("to")
    nip = report.get("nip")

    response_data = {
        "type": report_type,
        "kind": kind,
        "format": format_,
        "message": f"Report generated successfully for kind '{kind}' in format '{format_}'."
    }
    if trader_sys_number_EX:
        response_data["trader_sys_number_EX"] = trader_sys_number_EX
    if from_date and to_date:
        response_data["date_range"] = {"from": from_date, "to": to_date}
    if nip:
        response_data["nip"] = nip

    return jsonify({"packet": {"report": response_data}})
