import json

def force_transfer(data):
    packet = {
        "info": {
            "action": "teams_server",
            "server_action": "force_transfer"
        }
    }
    return simulate_server_response(packet)

def get_sent_receipts(data):
    packet = {
        "info": {
            "action": "teams_server",
            "server_action": "get"
        }
    }
    return simulate_server_response(packet)

def simulate_server_response(packet):
    if packet["info"]["server_action"] == "force_transfer":
        return {
            "info": {
                "action": "teams_server",
                "server_action": "force_transfer"
            }
        }
    elif packet["info"]["server_action"] == "get":
        return {
            "info": {
                "action": "teams_server",
                "server_action": "get",
                "jpk_send_count": "10",
                "jpk_actual_send_no": "0",
                "last_sent_receipt": "1",
                "receipt_to_send": "10"
            }
        }
