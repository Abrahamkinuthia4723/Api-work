import time
from flask import Flask, request, jsonify
import requests
from threading import Thread
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/non_fiscal_printout', methods=['POST'])
def non_fiscal_printout():
    data = request.data.decode('utf-8')
    
    try:
        root = ET.fromstring(data)  # Parse the XML data
        
        # Check if the non-fiscal printout tag exists
        non_fiscal_printout = root.find('non-fiscal_printout')
        if non_fiscal_printout is not None:
            system_number = non_fiscal_printout.get('system_number')
            qr_code = None
            lines = []

            for line in non_fiscal_printout.findall('line'):
                lines.append(line.text)
                if line.get('type') == 'qr_code':
                    qr_code = line.text

            # Respond based on the data received
            if qr_code and system_number is None:
                return jsonify({"message": "Non-fiscal printout with QR code processed successfully"})
            elif system_number and qr_code:
                return jsonify({"message": "Non-fiscal printout with system number and QR code processed successfully"})
            elif "<line></line>" in data:
                return jsonify({"message": "Non-fiscal printout with empty line and underline processed successfully"})
            else:
                return jsonify({"error": "Invalid non-fiscal printout data"}), 400
        else:
            return jsonify({"error": "Invalid non-fiscal printout data"}), 400
            
    except ET.ParseError:
        return jsonify({"error": "Invalid XML format"}), 400

@app.route('/send_non_fiscal_printout', methods=['POST'])
def send_non_fiscal_printout():
    packet = request.data.decode('utf-8')
    return jsonify({"message": "Non-fiscal printout packet received", "packet": packet}), 200

class PrinterAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_packet(self, packet):
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(self.base_url + "/send_non_fiscal_printout", data=packet, headers=headers)
        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid response, not JSON"}

    def send_non_fiscal_printout(self, system_number=None, lines=None, qr_code=None, barcode=None):
        lines_str = ""
        if lines:
            for line in lines:
                lines_str += f"<line type='line' font_number='1'>{line}</line>"

        qr_code_str = ""
        if qr_code:
            qr_code_str = f"""<line type="qr_code" bolded="yes" centered="yes" font_number="1" font_attribute="big">{qr_code}</line>"""
        
        barcode_str = ""
        if barcode:
            barcode_str = f"""<line type="barcode" bolded="yes" centered="yes" font_number="1" font_attribute="big">{barcode}</line>"""

        packet = f"""<packet>
                        <non-fiscal_printout system_number="{system_number}">
                            {lines_str}
                            {qr_code_str}
                            {barcode_str}
                        </non-fiscal_printout>
                    </packet>"""
        
        return self.send_packet(packet)

    def send_non_fiscal_with_empty_line_and_underline(self):
        packet = """<packet>
                        <non-fiscal_printout system_number="123" non-fiscal_printout_header="yes">
                            <line type="line" bolded="yes" negative="no" centered="yes" font_number="1" printout_on="copy" font_attribute="big">line1</line>
                            <line type="bolded"></line>
                            <line>line 3</line>
                            <line></line>
                            <line>line 4</line>
                        </non-fiscal_printout>
                    </packet>"""
        return self.send_packet(packet)

def main():
    printer_url = 'http://127.0.0.1:5001'
    printer_api = PrinterAPI(printer_url)

    print("Waiting for Flask server to start...")
    time.sleep(2)

    lines = ["line 1", "line 2", "line 3", "line 4", "line 5"]
    qr_code = "NOVITUS"
    response = printer_api.send_non_fiscal_printout(lines=lines, qr_code=qr_code)
    print("Non-Fiscal Printout with QR Code Response:", response)

    barcode = "123456789"
    response = printer_api.send_non_fiscal_printout(system_number="12345678", lines=lines, qr_code=qr_code, barcode=barcode)
    print("Non-Fiscal Printout with Multiple Lines, QR Code, and Barcode Response:", response)

    response = printer_api.send_non_fiscal_with_empty_line_and_underline()
    print("Non-Fiscal Printout with Empty Line and Underline Response:", response)

if __name__ == "__main__":
    def run_flask():
        app.run(debug=True, use_reloader=False, port=5001)

    thread = Thread(target=run_flask)
    thread.start()

    main()

