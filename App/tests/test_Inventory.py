import json
from App import create_app, db

class TestInventoryRoutes:
    @classmethod
    def setup_class(cls):
        cls.app = create_app("testing")
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def teardown_class(cls):
        with cls.app.app_context():
            db.drop_all()

    def test_get_all_inventory_items(self):
        # Positive Test: Ensure the GET /inventory/ route works
        response = self.client.get("/inventory/")
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_create_inventory_item(self):
        # Positive Test: Ensure the POST /inventory/ route works
        payload = {
            "item_name": "Brake Pads",
            "quantity": 50,
            "price": 25.99
        }
        response = self.client.post(
            "/inventory/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 201
        assert response.json["item_name"] == "Brake Pads"

    def test_create_inventory_item_invalid_data(self):
        # Negative Test: Test POST /inventory/ with invalid data
        payload = {
            "item_name": "",
            "quantity": -10,
            "price": "invalid_price"
        }
        response = self.client.post(
            "/inventory/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "error" in response.json

    def test_get_inventory_item_not_found(self):
        # Negative Test: Test GET /inventory/{item_id} with non-existent ID
        response = self.client.get("/inventory/999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_update_inventory_item(self):
        # Positive Test: Ensure the PUT /inventory/{item_id} route works
        # First, create an item
        payload = {
            "item_name": "Brake Pads",
            "quantity": 50,
            "price": 25.99
        }
        create_response = self.client.post(
            "/inventory/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        item_id = create_response.json["item_id"]

        # Update the item
        update_payload = {
            "quantity": 40,
            "price": 20.99
        }
        update_response = self.client.put(
            f"/inventory/{item_id}",
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        assert update_response.status_code == 200
        assert update_response.json["quantity"] == 40

    def test_delete_inventory_item(self):
        # Positive Test: Ensure the DELETE /inventory/{item_id} route works
        # First, create an item
        payload = {
            "item_name": "Brake Pads",
            "quantity": 50,
            "price": 25.99
        }
        create_response = self.client.post(
            "/inventory/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        item_id = create_response.json["item_id"]

        # Delete the item
        delete_response = self.client.delete(f"/inventory/{item_id}")
        assert delete_response.status_code == 200
        assert "message" in delete_response.json

    def test_delete_inventory_item_not_found(self):
        # Negative Test: Test DELETE /inventory/{item_id} with non-existent ID
        response = self.client.delete("/inventory/999")
        assert response.status_code == 404
        assert "error" in response.json