from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from App.models import ServiceTicket, Mechanics
from App.extensions import db
from .schemas import service_tickets_schema, service_ticket_schema

# Define the Blueprint for service tickets
service_tickets_bp = Blueprint('service_tickets', __name__)


# ROUTES — SERVICE TICKETS CRUD

# CREATE SERVICE TICKET
@service_tickets_bp.route("/", methods=["POST"])
def add_service_ticket():
    try:
        data = request.get_json() or {}

        # Validate and load the data using Marshmallow schema
        service_ticket_obj = service_ticket_schema.load(data)

        # Add the service ticket to the database
        db.session.add(service_ticket_obj)
        db.session.commit()

        return jsonify({
            "message": "Service ticket added successfully",
            "data": service_ticket_schema.dump(service_ticket_obj)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ASSIGN MECHANIC TO SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    try:
        # Fetch the service ticket and mechanic
        service_ticket = ServiceTicket.query.get(ticket_id)
        if not service_ticket:
            return jsonify({"error": "Service ticket not found"}), 404
        mechanic = Mechanics.query.get(mechanic_id)

        if not mechanic:
            return jsonify({"error": "Mechanic not found"}), 404

        # Assign the mechanic to the service ticket
        if mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
            db.session.commit()

        return jsonify({
            "message": "Mechanic assigned to service ticket successfully",
            "data": service_ticket_schema.dump(service_ticket)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# REMOVE MECHANIC FROM SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    try:
        # Fetch the service ticket and mechanic
        service_ticket = ServiceTicket.query.get(ticket_id)
        if not service_ticket:
            return jsonify({"error": "Service ticket not found"}), 404
        mechanic = Mechanics.query.get(mechanic_id)

        if not service_ticket:
            return jsonify({"error": "Service ticket not found"}), 404
        if not mechanic:
            return jsonify({"error": "Mechanic not found"}), 404

        # Remove the mechanic from the service ticket
        if mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
            db.session.commit()

        return jsonify({
            "message": "Mechanic removed from service ticket successfully",
            "data": service_ticket_schema.dump(service_ticket)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET all service tickets
@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    try:
        all_service_tickets = ServiceTicket.query.all()
        return jsonify(service_tickets_schema.dump(all_service_tickets)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET a single service ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_service_ticket(ticket_id):
    try:
        service_ticket = ServiceTicket.query.get(ticket_id)
        if not service_ticket:
            return jsonify({"message": "Service ticket not found"}), 404

        return jsonify(service_ticket_schema.dump(service_ticket)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE service ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_service_ticket(ticket_id):
    try:
        service_ticket = ServiceTicket.query.get(ticket_id)
        if not service_ticket:
            return jsonify({"message": "Service ticket not found"}), 404

        db.session.delete(service_ticket)
        db.session.commit()

        return jsonify({"message": "Service ticket deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE service ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
def update_service_ticket(ticket_id):
    try:
        # Parse the request data
        data = request.get_json()

        # Fetch the service ticket by ID
        service_ticket = ServiceTicket.query.get(ticket_id)
        if not service_ticket:
            return jsonify({"error": "Service ticket not found"}), 404

        # Update fields
        for key, value in data.items():
            if hasattr(service_ticket, key):
                setattr(service_ticket, key, value)

        db.session.commit()

        return jsonify({
            "message": "Service ticket updated successfully",
            "data": service_ticket_schema.dump(service_ticket)
        }), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------
@service_tickets_bp.route("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}, 200


print("ServiceTicket routes loaded")

def register_routes(app):
    print("register_routes function defined")
    # Example: Register blueprints or routes here
    from . import service_tickets_bp
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")