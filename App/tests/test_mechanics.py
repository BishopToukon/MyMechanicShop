import json
from App import create_app, db
from App.models import Mechanic

class TestMechanicRoutes:
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

    def test_get_all_mechanics(self):
        # Positive Test: Ensure the GET /mechanics/ route works
        response = self.client.get("/mechanics/")
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_create_mechanic(self):
        # Positive Test: Ensure the POST /mechanics/ route works
        payload = {
            "name": "John Mechanic",
            "address": "123 Mechanic St",
            "salary": 50000.00
        }
        response = self.client.post(
            "/mechanics/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 201
        assert response.json["name"] == "John Mechanic"

    def test_create_mechanic_invalid_data(self):
        # Negative Test: Test POST /mechanics/ with invalid data
        payload = {
            "name": "",
            "address": "",
            "salary": -1000
        }
        response = self.client.post(
            "/mechanics/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "error" in response.json

    def test_get_mechanic_not_found(self):
        # Negative Test: Test GET /mechanics/{mechanic_id} with non-existent ID
        response = self.client.get("/mechanics/999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_update_mechanic(self):
        # Positive Test: Ensure the PUT /mechanics/{mechanic_id} route works
        # First, create a mechanic
        payload = {
            "name": "John Mechanic",
            "address": "123 Mechanic St",
            "salary": 50000.00
        }
        create_response = self.client.post(
            "/mechanics/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        mechanic_id = create_response.json["mechanic_id"]

        # Update the mechanic
        update_payload = {
            "name": "Jane Mechanic",
            "salary": 60000.00
        }
        update_response = self.client.put(
            f"/mechanics/{mechanic_id}",
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        assert update_response.status_code == 200
        assert update_response.json["name"] == "Jane Mechanic"

    def test_update_mechanic_not_found(self):
        # Negative Test: Test PUT /mechanics/{mechanic_id} with non-existent ID
        update_payload = {
            "name": "Jane Mechanic",
            "salary": 60000.00
        }
        response = self.client.put(
            "/mechanics/999",
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        assert response.status_code == 404
        assert "error" in response.json

    def test_delete_mechanic(self):
        # Positive Test: Ensure the DELETE /mechanics/{mechanic_id} route works
        # First, create a mechanic
        payload = {
            "name": "John Mechanic",
            "address": "123 Mechanic St",
            "salary": 50000.00
        }
        create_response = self.client.post(
            "/mechanics/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        mechanic_id = create_response.json["mechanic_id"]

        # Delete the mechanic
        delete_response = self.client.delete(f"/mechanics/{mechanic_id}")
        assert delete_response.status_code == 200
        assert "message" in delete_response.json

    def test_delete_mechanic_not_found(self):
        # Negative Test: Test DELETE /mechanics/{mechanic_id} with non-existent ID
        response = self.client.delete("/mechanics/999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_get_mechanic_with_most_tickets(self):
        # Positive Test: Ensure the GET /mechanics/most-tickets route works
        response = self.client.get("/mechanics/most-tickets")
        assert response.status_code in [200, 404]  # 200 if mechanics exist, 404 if none exist