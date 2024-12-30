import sqlite3
from datetime import datetime
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify

app = Flask(__name__)

def create_db():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS fiscal_memory (
                        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report_date DATE,
                        event_details TEXT,
                        settlement_relief BOOLEAN,
                        tax_changes BOOLEAN,
                        daily_reports BOOLEAN)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS service_reviews (
                        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        review_date DATE,
                        service_name TEXT,
                        review_content TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_name TEXT,
                        event_date DATE,
                        event_details TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS protected_memory (
                        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report_type TEXT,
                        report_date DATE,
                        content TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS shifts (
                        shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cashier_name TEXT,
                        income REAL,
                        expense REAL,
                        cash REAL,
                        payin REAL,
                        payout REAL,
                        balance REAL,
                        receipt_count INTEGER,
                        canceled_receipt_count INTEGER,
                        storno_count INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        shift_id INTEGER,
                        payment_name TEXT,
                        payment_value REAL,
                        payment_type TEXT,
                        FOREIGN KEY (shift_id) REFERENCES shifts(shift_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS containers (
                        container_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        shift_id INTEGER,
                        container_type TEXT,
                        container_value REAL,
                        FOREIGN KEY (shift_id) REFERENCES shifts(shift_id))''')

    cursor.execute('''INSERT INTO fiscal_memory (report_date, event_details, settlement_relief, tax_changes, daily_reports)
                      VALUES ('2004-06-04', 'Detailed Event #1', 1, 1, 1),
                             ('2004-06-05', 'Detailed Event #2', 1, 0, 1),
                             ('2004-06-06', 'Detailed Event #3', 0, 1, 0)''')

    cursor.execute('''INSERT INTO service_reviews (review_date, service_name, review_content)
                      VALUES ('2004-06-04', 'Service A', 'Excellent Service!'),
                             ('2004-06-05', 'Service B', 'Good Service.'),
                             ('2004-06-06', 'Service C', 'Average Service.')''')

    cursor.execute('''INSERT INTO events (event_name, event_date, event_details)
                      VALUES ('Event #1', '2004-06-04', 'Details of Event #1'),
                             ('Event #2', '2004-06-05', 'Details of Event #2'),
                             ('Event #3', '2004-06-06', 'Details of Event #3')''')

    cursor.execute('''INSERT INTO protected_memory (report_type, report_date, content)
                      VALUES ('receipt', '2004-06-04', 'Receipt #001 Content'),
                             ('invoice', '2004-06-05', 'Invoice #123 Content'),
                             ('daily_report', '2004-06-06', 'Daily Report Content'),
                             ('non_fiscal', '2004-06-07', 'Non-Fiscal Printout Content'),
                             ('all', '2004-06-08', 'All Printouts Content')''')

    cursor.execute('''INSERT INTO shifts (cashier_name, income, expense, cash, payin, payout, balance, receipt_count, canceled_receipt_count, storno_count)
                      VALUES ('Jan', 10, 10, 23.23, 40, 10, 30, 12, 1, 0)''')
    shift_id = cursor.lastrowid
    cursor.execute('''INSERT INTO payments (shift_id, payment_name, payment_value, payment_type)
                      VALUES (?, 'gift card', 234.12, 'card')''', (shift_id,))
    cursor.execute('''INSERT INTO containers (shift_id, container_type, container_value)
                      VALUES (?, 'out', 23)''', (shift_id,))

    conn.commit()
    conn.close()

def generate_report_packet(report_type, **kwargs):
    packet = f'<packet><report type="{report_type}"'
    packet += ''.join([f' {key}="{value}"' for key, value in kwargs.items()])
    packet += f'></report></packet>'
    return packet

def process_packet(data):
    report_type = data.get('type')

    if report_type == "daily":
        date = data.get('date', datetime.now().strftime('%d-%m-%Y'))
        return f"Generating daily report for {date}"
    elif report_type == "periodical":
        from_date = data.get('from_date', '')
        to_date = data.get('to', '')
        checkbox_no = data.get('checkbox_no', '')
        cashier = data.get('cashier', '')
        kind = data.get('kind', 'full')
        return f"Generating periodical report from {from_date} to {to_date}, for cashier {cashier}, kind: {kind}"
    elif report_type == "cash":
        cashier = data.get('cashier', '')
        income = data.get('income', 0)
        expense = data.get('expense', 0)
        cash = data.get('cash', 0)
        payin = data.get('payin', 0)
        payout = data.get('payout', 0)
        balance = data.get('balance', 0)
        return f"Generating shift report for cashier {cashier} with income {income}, expense {expense}"
    elif report_type == "service_review":
        return "Generating service review report"
    elif report_type == "events":
        return "Generating events report"
    elif report_type == "protected_memory":
        report_type = data.get('kind', 'all')
        return f"Generating protected memory report for type {report_type}"
    else:
        return "Unsupported report type"

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    result = process_packet(data)
    return jsonify({"message": result})

if __name__ == "__main__":
    create_db()
    app.run(debug=True)
