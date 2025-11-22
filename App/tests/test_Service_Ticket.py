import json
from App import create_app, db
from App.models import ServiceTicket

class TestServiceTicketRoutes:
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

    def test_get_all_service_tickets(self):
        # Positive Test: Ensure the GET /tickets/ route works
        response = self.client.get("/tickets/")
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_create_service_ticket(self):
        # Positive Test: Ensure the POST /tickets/ route works
        payload = {
            "description": "Oil change",
            "date": "2023-11-01T10:00:00",
            "customer_id": 1
        }
        response = self.client.post(
            "/tickets/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 201
        assert response.json["description"] == "Oil change"

    def test_create_service_ticket_invalid_data(self):
        # Negative Test: Test POST /tickets/ with invalid data
        payload = {
            "description": "",
            "date": "invalid-date",
            "customer_id": "not-an-integer"
        }
        response = self.client.post(
            "/tickets/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "error" in response.json

    def test_get_service_ticket_not_found(self):
        # Negative Test: Test GET /tickets/{ticket_id} with non-existent ID
        response = self.client.get("/tickets/999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_update_service_ticket(self):
        # Positive Test: Ensure the PUT /tickets/{ticket_id}/edit route works
        # First, create a ticket
        payload = {
            "description": "Oil change",
            "date": "2023-11-01T10:00:00",
            "customer_id": 1
        }
        create_response = self.client.post(
            "/tickets/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        ticket_id = create_response.json["ticket_id"]

        # Update the ticket
        update_payload = {
            "description": "Brake replacement",
            "date": "2023-11-02T15:00:00"
        }
        update_response = self.client.put(
            f"/tickets/{ticket_id}/edit",
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        assert update_response.status_code == 200
        assert update_response.json["description"] == "Brake replacement"

    def test_update_service_ticket_not_found(self):
        # Negative Test: Test PUT /tickets/{ticket_id}/edit with non-existent ID
        update_payload = {
            "description": "Brake replacement",
            "date": "2023-11-02T15:00:00"
        }
        response = self.client.put(
            "/tickets/999/edit",
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        assert response.status_code == 404
        assert "error" in response.json

    def test_delete_service_ticket(self):
        # Positive Test: Ensure the DELETE /tickets/{ticket_id} route works
        # First, create a ticket
        payload = {
            "description": "Oil change",
            "date": "2023-11-01T10:00:00",
            "customer_id": 1
        }
        create_response = self.client.post(
            "/tickets/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        ticket_id = create_response.json["ticket_id"]

        # Delete the ticket
        delete_response = self.client.delete(f"/tickets/{ticket_id}")
        assert delete_response.status_code == 200
        assert "message" in delete_response.json

    def test_delete_service_ticket_not_found(self):
        # Negative Test: Test DELETE /tickets/{ticket_id} with non-existent ID
        response = self.client.delete("/tickets/999")
        assert response.status_code == 404
        assert "error" in response.json