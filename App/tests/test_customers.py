import json
from App import create_app, db
from App.models import Customer

class TestCustomerRoutes:
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

    def test_get_all_customers(self):
        # Positive Test: Ensure the GET /customers/ route works
        response = self.client.get("/customers/")
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_create_customer(self):
        # Positive Test: Ensure the POST /customers/ route works
        payload = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "1234567890"
        }
        response = self.client.post(
            "/customers/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 201
        assert response.json["name"] == "John Doe"

    def test_create_customer_invalid_data(self):
        # Negative Test: Test POST /customers/ with invalid data
        payload = {
            "name": "",
            "email": "invalid-email",
            "phone": "not-a-phone-number"
        }
        response = self.client.post(
            "/customers/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "error" in response.json

    def test_get_customer_not_found(self):
        # Negative Test: Test GET /customers/{customer_id} with non-existent ID
        response = self.client.get("/customers/999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_update_customer(self):
        # Positive Test: Ensure the PUT /customers/{customer_id} route works
        # First, create a customer
        payload = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "1234567890"
        }
        create_response = self.client.post(
            "/customers/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        customer_id = create_response.json["customer_id"]

        # Update the customer
        update_payload = {
            "name": "Jane Doe",
            "email": "janedoe@example.com"
        }
        update_response = self.client.put(
            f"/customers/{customer_id}",
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        assert update_response.status_code == 200
        assert update_response.json["name"] == "Jane Doe"

    def test_update_customer_not_found(self):
        # Negative Test: Test PUT /customers/{customer_id} with non-existent ID
        update_payload = {
            "name": "Jane Doe",
            "email": "janedoe@example.com"
        }
        response = self.client.put(
            "/customers/999",
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        assert response.status_code == 404
        assert "error" in response.json

    def test_delete_customer(self):
        # Positive Test: Ensure the DELETE /customers/{customer_id} route works
        # First, create a customer
        payload = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "1234567890"
        }
        create_response = self.client.post(
            "/customers/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        customer_id = create_response.json["customer_id"]

        # Delete the customer
        delete_response = self.client.delete(f"/customers/{customer_id}")
        assert delete_response.status_code == 200
        assert "message" in delete_response.json

    def test_delete_customer_not_found(self):
        # Negative Test: Test DELETE /customers/{customer_id} with non-existent ID
        response = self.client.delete("/customers/999")
        assert response.status_code == 404
        assert "error" in response.json