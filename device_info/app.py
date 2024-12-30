from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///device_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Device Table
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    module_printer_version = db.Column(db.String(50), nullable=False)
    system_name = db.Column(db.String(50), nullable=False)
    system_version = db.Column(db.String(20), nullable=False)
    display_count = db.Column(db.Integer, nullable=False)
    display_len = db.Column(db.Integer, nullable=False)
    ecopy = db.Column(db.Integer, nullable=False)
    fiscal_size = db.Column(db.Integer, nullable=False)

# FiscalMemory Table
class FiscalMemory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fiscal_size = db.Column(db.Integer, nullable=False)
    record_len = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    unique_no = db.Column(db.String(50))
    nip = db.Column(db.String(50))
    event_len = db.Column(db.Integer, nullable=False)
    record_count = db.Column(db.Integer, nullable=False)
    max_daily_report_count = db.Column(db.Integer, nullable=False)
    daily_report_count = db.Column(db.Integer, nullable=False)
    resets_max_count = db.Column(db.Integer, nullable=False)
    resets_count = db.Column(db.Integer, nullable=False)
    max_tax_rates_count = db.Column(db.Integer, nullable=False)
    tax_rates_count = db.Column(db.Integer, nullable=False)
    currency_change_max_count = db.Column(db.Integer, nullable=False)
    currency_change_count = db.Column(db.Integer, nullable=False)
    fiscalization_date = db.Column(db.String(20))
    fiscal_mode_close_date = db.Column(db.String(20))
    currency_name = db.Column(db.String(20))

# Power Information Table
class PowerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    power_mode = db.Column(db.Integer, nullable=False)
    power_supply_voltage = db.Column(db.Integer, nullable=False)
    power_accumulator_voltage = db.Column(db.Integer, nullable=False)
    power_battery_voltage = db.Column(db.Integer, nullable=False)
    accumulator_state = db.Column(db.Integer, nullable=False)
    battery_state = db.Column(db.Integer, nullable=False)
    charge_level_accumulator = db.Column(db.Integer, nullable=False)

# Printer Information Table
class PrinterInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    printer_module_version = db.Column(db.String(50), nullable=False)
    printer_len = db.Column(db.Integer, nullable=False)
    printer_len_mm = db.Column(db.Integer, nullable=False)
    font = db.Column(db.String(20), nullable=False)
    cutter = db.Column(db.String(20), nullable=False)
    paper_count = db.Column(db.Integer, nullable=False)

# Drawer Information Table
class DrawerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drawer_state = db.Column(db.String(20), nullable=False)

# Database State Table
class DatabaseState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_article_state = db.Column(db.Integer, nullable=False)

# Initialize and seed database
def init_db():
    with app.app_context():
        db.create_all()

        if Device.query.count() == 0:
            device = Device(
                device_name="HD Online",
                version="1.00",
                module_printer_version="CITIZ",
                system_name="OES",
                system_version="1.00",
                display_count=2,
                display_len=64,
                ecopy=1,
                fiscal_size=1048576
            )
            db.session.add(device)

        if FiscalMemory.query.count() == 0:
            fiscal_memory = FiscalMemory(
                fiscal_size=1048576,
                record_len=940,
                mode=0,
                unique_no="1234567890",
                nip="9876543210",
                event_len=2108,
                record_count=6,
                max_daily_report_count=1830,
                daily_report_count=0,
                resets_max_count=200,
                resets_count=0,
                max_tax_rates_count=30,
                tax_rates_count=0,
                currency_change_max_count=20,
                currency_change_count=0,
                fiscalization_date="2000-00-00 00:00:00",
                fiscal_mode_close_date="2000-00-00 00:00:00",
                currency_name="PLN"
            )
            db.session.add(fiscal_memory)

        if PowerInfo.query.count() == 0:
            power_info = PowerInfo(
                power_mode=1,
                power_supply_voltage=25,
                power_accumulator_voltage=25,
                power_battery_voltage=25,
                accumulator_state=2,
                battery_state=2,
                charge_level_accumulator=75
            )
            db.session.add(power_info)

        if PrinterInfo.query.count() == 0:
            printer_info = PrinterInfo(
                printer_module_version="CITIZ",
                printer_len=64,
                printer_len_mm=80,
                font="normal",
                cutter="yes",
                paper_count=1
            )
            db.session.add(printer_info)

        if DrawerInfo.query.count() == 0:
            drawer_info = DrawerInfo(
                drawer_state="drawer_close"
            )
            db.session.add(drawer_info)

        if DatabaseState.query.count() == 0:
            db_state = DatabaseState(
                db_article_state=0
            )
            db.session.add(db_state)

        db.session.commit()

@app.route('/device_info', methods=['GET'])
def get_device_info():
    # Collect general device info
    device = Device.query.first()
    if device:
        response = f'''<packet>
                        <device_info action="general"
                                     device_name="{device.device_name}"
                                     version="{device.version}"
                                     module_printer_version="{device.module_printer_version}"
                                     system_name="{device.system_name}"
                                     system_version="{device.system_version}"
                                     display_count="{device.display_count}"
                                     display_len="{device.display_len}"
                                     ecopy="{device.ecopy}"
                                     fiscal_size="{device.fiscal_size}" />
                    </packet>'''
        return Response(response, mimetype='application/xml')
    return jsonify({"message": "Device info not found"}), 404

@app.route('/device_info/detail_fiscal_memory_info', methods=['GET'])
def get_fiscal_memory_info():
    fiscal_memory = FiscalMemory.query.first()
    if fiscal_memory:
        response = f'''<packet>
                        <device_info action="detail_fiscal_memory_info"
                                     fiscal_size="{fiscal_memory.fiscal_size}"
                                     record_len="{fiscal_memory.record_len}"
                                     mode="{fiscal_memory.mode}"
                                     unique_no="{fiscal_memory.unique_no}"
                                     nip="{fiscal_memory.nip}"
                                     event_len="{fiscal_memory.event_len}"
                                     record_count="{fiscal_memory.record_count}"
                                     max_daily_report_count="{fiscal_memory.max_daily_report_count}"
                                     daily_report_count="{fiscal_memory.daily_report_count}"
                                     resets_max_count="{fiscal_memory.resets_max_count}"
                                     resets_count="{fiscal_memory.resets_count}"
                                     max_tax_rates_count="{fiscal_memory.max_tax_rates_count}"
                                     tax_rates_count="{fiscal_memory.tax_rates_count}"
                                     currency_change_max_count="{fiscal_memory.currency_change_max_count}"
                                     currency_change_count="{fiscal_memory.currency_change_count}"
                                     fiscalization_date="{fiscal_memory.fiscalization_date}"
                                     fiscal_mode_close_date="{fiscal_memory.fiscal_mode_close_date}"
                                     currency_name="{fiscal_memory.currency_name}" />
                    </packet>'''
        return Response(response, mimetype='application/xml')
    return jsonify({"message": "Fiscal memory info not found"}), 404

@app.route('/device_info/battery_info', methods=['GET'])
def get_battery_info():
    power_info = PowerInfo.query.first()
    if power_info:
        response = f'''<packet>
                        <device_info action="battery_info"
                                     power_accumulator_voltage="{power_info.power_accumulator_voltage}"
                                     power_supply_voltage="{power_info.power_supply_voltage}"
                                     power_battery_voltage="{power_info.power_battery_voltage}"
                                     power_supply="yes" />
                    </packet>'''
        return Response(response, mimetype='application/xml')
    return jsonify({"message": "Power info not found"}), 404

@app.route('/device_info/printout_info', methods=['GET'])
def get_printout_info():
    printer_info = PrinterInfo.query.first()
    if printer_info:
        response = f'''<packet>
                        <device_info action="printout_info"
                                     printer_module_version="{printer_info.printer_module_version}"
                                     printer_len="{printer_info.printer_len}"
                                     printer_len_mm="{printer_info.printer_len_mm}"
                                     font="{printer_info.font}"
                                     cutter="{printer_info.cutter}"
                                     paper_count="{printer_info.paper_count}" />
                    </packet>'''
        return Response(response, mimetype='application/xml')
    return jsonify({"message": "Printer info not found"}), 404

@app.route('/device_info/drawer_state', methods=['GET'])
def get_drawer_state():
    drawer_info = DrawerInfo.query.first()
    if drawer_info:
        response = f'''<packet>
                        <device_info action="drawer_state"
                                     drawer_state="{drawer_info.drawer_state}" />
                    </packet>'''
        return Response(response, mimetype='application/xml')
    return jsonify({"message": "Drawer state not found"}), 404

@app.route('/device_info/db_article_state', methods=['GET'])
def get_db_article_state():
    db_state = DatabaseState.query.first()
    if db_state:
        response = f'''<packet>
                        <device_info action="db_article_state"
                                     db_article_state="{db_state.db_article_state}" />
                    </packet>'''
        return Response(response, mimetype='application/xml')
    return jsonify({"message": "Database article state not found"}), 404

@app.route('/device_info/power_info', methods=['GET'])
def get_power_info():
    power_info = PowerInfo.query.first()
    if power_info:
        response = f'''<packet>
                        <device_info action="power_info"
                                     power_mode="{power_info.power_mode}"
                                     power_supply_voltage="{power_info.power_supply_voltage}"
                                     power_accumulator_voltage="{power_info.power_accumulator_voltage}"
                                     power_battery_voltage="{power_info.power_battery_voltage}"
                                     accumulator_state="{power_info.accumulator_state}"
                                     battery_state="{power_info.battery_state}"
                                     charge_level_accumulator="{power_info.charge_level_accumulator}" />
                    </packet>'''
        return Response(response, mimetype='application/xml')
    return jsonify({"message": "Power info not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
