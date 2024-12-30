import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

def get_current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M")

@app.route('/log_pl', methods=['POST'])
def log_pl():
    try:
        data = request.data.decode('utf-8')
        root = ET.fromstring(data)

        if root.tag != 'packet':
            return jsonify(status="error", message="Invalid packet format."), 400

        log_pl_element = root.find('log_pl')
        if log_pl_element is None:
            return jsonify(status="error", message="Missing <log_pl> tag."), 400

        action = log_pl_element.get('action')
        port = log_pl_element.get('port')

        if action == 'read':
            if port:
                return jsonify(
                    status="success",
                    message=f"Reading data from {port}.",
                    data="dane....",
                    action=action,
                    port=port,
                    date=get_current_datetime()
                )
            else:
                return jsonify(
                    status="success",
                    message="Reading data from all ports.",
                    data="dane....",
                    action=action,
                    date=get_current_datetime()
                )
        
        elif action == 'write':
            if port:
                return jsonify(
                    status="success",
                    message=f"Writing data to {port}.",
                    data="dane....",
                    action=action,
                    port=port,
                    date=get_current_datetime()
                )
            else:
                return jsonify(
                    status="success",
                    message="Writing data to all ports.",
                    data="dane....",
                    action=action,
                    date=get_current_datetime()
                )

        else:
            return jsonify(status="error", message="Invalid action."), 400

    except ET.ParseError:
        return jsonify(status="error", message="Invalid XML format."), 400

@app.route('/non_fiscal_printout', methods=['POST'])
def non_fiscal_printout():
    try:
        data = request.data.decode('utf-8')
        root = ET.fromstring(data)

        if root.tag != 'packet':
            return jsonify(status="error", message="Invalid packet format."), 400

        non_fiscal_printout_element = root.find('non-fiscal_printout')
        if non_fiscal_printout_element is None:
            return jsonify(status="error", message="Missing <non-fiscal_printout> tag."), 400

        system_no = non_fiscal_printout_element.get('system_no')
        non_fiscal_header = non_fiscal_printout_element.get('non-fiscal_header')

        lines = []
        for line_element in non_fiscal_printout_element.findall('line'):
            line_type = line_element.get('type')
            line_text = line_element.text
            lines.append({
                "type": line_type,
                "content": line_text,
                "attributes": {
                    "bold": line_element.get('bold'),
                    "inwers": line_element.get('inwers'),
                    "center": line_element.get('center'),
                    "font_id": line_element.get('font_id'),
                    "font_attr": line_element.get('font_attr'),
                    "print_on": line_element.get('print_on')
                }
            })

        # Return the non-fiscal printout data
        return jsonify(
            status="success",
            message="Non-fiscal printout performed successfully.",
            system_no=system_no,
            non_fiscal_header=non_fiscal_header,
            lines=lines
        )

    except ET.ParseError:
        return jsonify(status="error", message="Invalid XML format."), 400

if __name__ == '__main__':
    app.run(debug=True)
