from datetime import datetime

SERVER_DATA = {
    "action": "teams_server",
    "server_action": "get",
    "jpk_send_count": 10,
    "jpk_actual_send_no": 0,
    "last_sent_receipt": 1,
    "receipt_to_send": 10
}

RECEIPT_DATA = {
    "start": {
        "action": "begin",
        "mode": "online",
        "pharmaceutical": "no",
        "type": "tax_invoice",
        "relevant_receipt_number": 0,
        "nip": "A123456123B"
    }
}

QR_DATA = {
    1: {
        "receipt_number": 1,
        "middleware_invoice_number": "0100099410000000001",
        "qr_code_link": "https://tims-test.kra.go.ke/KRA-Portal/invoiceChk.htm?actionCode=loadPage&invoiceNo="
    }
}

STATUS_DATA = {
    "action": "checkout",
    "type": "receipt",
    "lasterror": "0",
    "isfiscal": "yes",
    "receiptopen": "no",
    "lastreceipterror": "no",
    "resetcount": "0",
    "date": "08-10-2013",
    "receiptcount": "11",
    "cash": "444.76",
    "uniqueno": "ABC12345678",
    "lastreceipt": "11",
    "lastinvoice": "1",
    "lastprintout": "47",
    "cycles": "1130909187",
    "seconds": "180",
    "begin_date": "2000-00-00 00:00:00",
    "receipt_count_in_report": "1",
    "ptu": {
        "A": "12.50",
        "B": "0.00",
        "C": "0.00",
        "D": "0.00",
        "G": "0.00"
    }
}
