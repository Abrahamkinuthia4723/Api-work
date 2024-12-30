class Receipt:
    @staticmethod
    def get_receipt_by_number(receipt_number):
        return {
            "packet": {
                "info": {
                    "action": "receipt",
                    "receipt_number": receipt_number,
                    "trader_sys_number": "123/ab234",
                    "middleware_invoice_number": "0100102790000000005",
                    "qr_code_link": "https://tims-test.kra.go.ke/KRA-Portal/invoiceChk.htm?actionCode=loadPage&invoiceNo=",
                    "CU_number": "KRAMW010202204010279"
                }
            }
        }

    @staticmethod
    def get_receipt_by_trader_sys_number(trader_sys_number):
        return {
            "packet": {
                "info": {
                    "action": "receipt",
                    "trader_sys_number_EX": trader_sys_number,
                    "middleware_invoice_number": "0100102790000000005",
                    "qr_code_link": "https://tims-test.kra.go.ke/KRA-Portal/invoiceChk.htm?actionCode=loadPage&invoiceNo=",
                    "CU_number": "KRAMW010202204010279"
                }
            }
        }

    @staticmethod
    def get_last_signed_receipt():
        return {
            "packet": {
                "info": {
                    "action": "last_receipt",
                    "last_receipt_number": "1001"
                }
            }
        }

class Report:
    @staticmethod
    def generate_report_by_trader_sys_number(trader_sys_number):
        return {
            "packet": {
                "report": {
                    "type": "protectedmemory",
                    "trader_sys_number_EX": trader_sys_number,
                    "kind": "receipt_by_trad_sys_num",
                    "format": "standard"
                }
            }
        }

class PrinterData:
    @staticmethod
    def get_data_by_trader_sys_number(trader_sys_number):
        return {
            "packet": {
                "info": {
                    "action": "receipt",
                    "trader_sys_number_EX": trader_sys_number,
                    "qr_code_link": "https://tims-test.kra.go.ke/KRA-Portal/invoiceChk.htm?actionCode=loadPage&invoiceNo=",
                    "CU_number": "KRAMW010202204010279"
                }
            }
        }
