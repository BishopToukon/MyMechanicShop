import unittest
import json
from App import create_app, db
from App.models import Inventory

class TestInventoryRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.payload = {
            "item_name": "Brake Pads",
            "quantity": 50,
            "price": 25.99
        }

    def test_create_inventory_item(self):
        response = self.client.post(
            "/inventory/",
            data=json.dumps(self.payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("data", response.json)
        self.assertEqual(response.json["data"]["item_name"], "Brake Pads")

    def test_get_all_inventory_items(self):
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_inventory_item_invalid_data(self):
        invalid_payload = {
            "item_name": "",
            "quantity": -10,
            "price": "invalid_price"
        }
        response = self.client.post(
            "/inventory/",
            data=json.dumps(invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_delete_inventory_item(self):
        # Create an item first
        create_response = self.client.post(
            "/inventory/",
            data=json.dumps(self.payload),
            content_type="application/json"
        )
        item_id = create_response.json["data"]["item_id"]

        # Delete the item
        delete_response = self.client.delete(f"/inventory/{item_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn("message", delete_response.json)

    def test_delete_inventory_item_not_found(self):
        response = self.client.delete("/inventory/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)