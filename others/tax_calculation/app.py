from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

tax_data = {
    "t_leavy": 0,
    "s_charge": 0,
    "total_to_pay": 0.0
}

@app.route('/set_tax', methods=['POST'])
def set_tax():
    try:
        data = request.get_json()
        required_fields = ['type', 'value']
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        tax_type = data['type']
        value = float(data['value'])
        
        if tax_type not in ['t_leavy', 's_charge']:
            return jsonify({"error": f"Invalid tax type: {tax_type}"}), 400
        
        tax_data[tax_type] = value
        
        tax_data['total_to_pay'] = 10.00 + tax_data['t_leavy'] + tax_data['s_charge']
        
        response_packet = {
            "tax": {
                "action": "set",
                "type": tax_type,
                "value": value
            }
        }
        
        return jsonify(response_packet), 200
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/get_tax', methods=['GET'])
def get_tax():
    try:
        response_packet = {
            "tax": {
                "action": "get",
                "total_to_pay": tax_data['total_to_pay']
            }
        }
        
        return jsonify(response_packet), 200
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
