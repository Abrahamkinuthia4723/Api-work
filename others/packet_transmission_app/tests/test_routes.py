import unittest
from app import app

class TeamsServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_force_transfer(self):
        payload = {
            "info": {
                "action": "teams_server",
                "server_action": "force_transfer"
            }
        }
        response = self.app.post('/teams_server/force_transfer', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("force_transfer", str(response.data))

    def test_get_sent_receipts(self):
        payload = {
            "info": {
                "action": "teams_server",
                "server_action": "get"
            }
        }
        response = self.app.post('/teams_server/get_receipts', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("jpk_send_count", str(response.data))
        self.assertIn("jpk_actual_send_no", str(response.data))

if __name__ == '__main__':
    unittest.main()
