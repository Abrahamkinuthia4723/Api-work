import unittest
from app import create_app

class ProtectedMemoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_generate_report_with_valid_payload(self):
        payload = {
            "report": {
                "type": "protectedmemory",
                "kind": "receipt",
                "format": "standard",
                "from": "04-06-2004",
                "to": "06-06-2006",
                "nip": "A123456123B"
            }
        }
        response = self.client.post('/protectedmemory/', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("packet", response.json)

    def test_generate_report_with_invalid_payload(self):
        payload = {
            "report": {
                "type": "invalidtype",
                "kind": "receipt",
                "format": "standard"
            }
        }
        response = self.client.post('/protectedmemory/', json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
