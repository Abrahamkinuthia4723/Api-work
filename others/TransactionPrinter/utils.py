from datetime import datetime
import random

def create_response_json(from_num, to_num, kind, format, action, receipt_number):
    """
    Creates a JSON response packet.
    """
    response = {
        "packet": {
            "report": {
                "type": "protectedmemory",
                "from": from_num,
                "to": to_num,
                "kind": kind,
                "format": format,
                "action": action,
                "receipt_number": receipt_number,
                "printout": f"Receipt {receipt_number} details go here"
            }
        }
    }
    return response

def validate_date(date_str):
    """
    Validates and converts a string to a datetime object in dd-mm-yyyy format.
    """
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}, expected dd-mm-yyyy")
