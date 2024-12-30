from flask import Flask, request, jsonify
import requests
from threading import Thread

# Flask application setup
app = Flask(__name__)

# In-memory data store for the mock API
printer_data = {
    "printed_paper_count": 1000,  # Initial count for printed paper
    "drawer_openings_count": 50,  # Initial count for drawer openings
}

# Endpoint to get printed paper info (read or reset)
@app.route('/printed_paper', methods=['POST'])
def get_printed_paper():
    data = request.data.decode('utf-8')
    if "<paper action=\"read\">" in data:
        return jsonify({"printed_paper_count": printer_data["printed_paper_count"]})
    elif "<paper action=\"reset\">" in data:
        printer_data["printed_paper_count"] = 0
        return jsonify({"message": "Printed paper count reset"})
    else:
        return jsonify({"error": "Invalid action"}), 400

# Endpoint to get drawer opening info (read or reset)
@app.route('/drawer_counter', methods=['POST'])
def get_drawer_counter():
    data = request.data.decode('utf-8')
    if "<drawer_counter action=\"read\">" in data:
        return jsonify({"drawer_openings_count": printer_data["drawer_openings_count"]})
    elif "<drawer_counter action=\"reset\">" in data:
        printer_data["drawer_openings_count"] = 0
        return jsonify({"message": "Drawer openings count reset"})
    else:
        return jsonify({"error": "Invalid action"}), 400

# Endpoint for sending a non-fiscal printout
@app.route('/non_fiscal_printout', methods=['POST'])
def non_fiscal_printout():
    data = request.data.decode('utf-8')
    if "<non-fiscal_printout" in data:
        return jsonify({"message": "Non-fiscal printout sent successfully"})
    else:
        return jsonify({"error": "Invalid non-fiscal printout data"}), 400

# Endpoint to handle graphic programming commands
@app.route('/graphic', methods=['POST'])
def graphic_programming():
    data = request.data.decode('utf-8')
    if "<graphic action=\"program\"" in data:
        return jsonify({"message": "Graphic programming data received"})
    elif "<graphic action=\"delete\"" in data:
        return jsonify({"message": "Graphic deleted"})
    else:
        return jsonify({"error": "Invalid graphic command"}), 400


# PrinterAPI class to interact with the Flask API
class PrinterAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_packet(self, packet):
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(self.base_url, data=packet, headers=headers)
        return response.json()

    def get_printed_paper_info(self):
        packet = """<packet>
                        <paper action="read"></paper>
                    </packet>"""
        return self.send_packet(packet)

    def reset_printed_paper_info(self):
        packet = """<packet>
                        <paper action="reset"></paper>
                    </packet>"""
        return self.send_packet(packet)

    def get_drawer_opening_info(self):
        packet = """<packet>
                        <drawer_counter action="read"></drawer_counter>
                    </packet>"""
        return self.send_packet(packet)

    def reset_drawer_opening_info(self):
        packet = """<packet>
                        <drawer_counter action="reset"></drawer_counter>
                    </packet>"""
        return self.send_packet(packet)

    def send_non_fiscal_printout(self, system_number, line_text):
        packet = f"""<packet>
                        <non-fiscal_printout system_number="{system_number}">
                            <line type="line" font_number="1">{line_text}</line>
                        </non-fiscal_printout>
                    </packet>"""
        return self.send_packet(packet)

    def program_graphic(self, graphic_data, graphic_id=1, graphic_type="all"):
        packet = f"""<packet>
                        <graphic action="program" id="{graphic_id}" type="{graphic_type}">
                            {graphic_data}
                        </graphic>
                    </packet>"""
        return self.send_packet(packet)

    def delete_graphic(self, graphic_id=1):
        packet = f"""<packet>
                        <graphic action="delete" id="{graphic_id}"></graphic>
                    </packet>"""
        return self.send_packet(packet)


def main():
    printer_url = 'http://127.0.0.1:5000'  

    # Initialize Printer API
    printer_api = PrinterAPI(printer_url)

    # Get printed paper information
    printed_paper_info = printer_api.get_printed_paper_info()
    print("Printed Paper Info:", printed_paper_info)

    # Reset printed paper counter
    reset_paper_info = printer_api.reset_printed_paper_info()
    print("Reset Printed Paper Info:", reset_paper_info)

    #  Get drawer opening count
    drawer_info = printer_api.get_drawer_opening_info()
    print("Drawer Opening Info:", drawer_info)

    # Reset drawer opening counter
    reset_drawer_info = printer_api.reset_drawer_opening_info()
    print("Reset Drawer Opening Info:", reset_drawer_info)

    # Send non-fiscal printout with multiple spaces
    system_number = "12345678"
    line_text = "Novi &#32;&#32;&#32;&#32;&#32;&#32;&#32;tus"
    non_fiscal_response = printer_api.send_non_fiscal_printout(system_number, line_text)
    print("Non-Fiscal Printout Response:", non_fiscal_response)

    # Program a graphic
    graphic_data = "012C003CFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF" * 2 
    graphic_response = printer_api.program_graphic(graphic_data)
    print("Graphic Programming Response:", graphic_response)

    # Delete a graphic
    delete_graphic_response = printer_api.delete_graphic()
    print("Graphic Deletion Response:", delete_graphic_response)


if __name__ == "__main__":
    def run_flask():
        app.run(debug=True, use_reloader=False)

    thread = Thread(target=run_flask)
    thread.start()

    main()
