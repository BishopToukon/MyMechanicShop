from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from App.models import ServiceTicket, Mechanics
from App.extensions import db, limiter, cache
from App.utils.util import token_required
from .schemas import service_tickets_schema, service_ticket_schema, mechanic_schema, mechanics_schema

# Define the Blueprint for service tickets
service_tickets_bp = Blueprint('service_tickets', __name__)
mechanics_bp = Blueprint('mechanics', __name__)


# ROUTES — SERVICE TICKETS CRUD

# CREATE SERVICE TICKET
@service_tickets_bp.route("/", methods=["POST"])
@token_required
def add_service_ticket(customer_id):
    try:
        data = request.get_json() or {}

        # Add the customer_id from the token to the data
        data["customer_id"] = customer_id

        # Validate and load the data using Marshmallow schema
        service_ticket_obj = service_ticket_schema.load(data)

        # Add the service ticket to the database
        db.session.add(service_ticket_obj)
        db.session.commit()

        return jsonify({
            "message": "Service ticket created successfully",
            "data": service_ticket_schema.dump(service_ticket_obj)
        }), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
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


# EDIT MECHANICS IN SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
def edit_mechanics(ticket_id):
    try:
        data = request.get_json() or {}
        add_ids = data.get("add_ids", [])
        remove_ids = data.get("remove_ids", [])

        # Fetch the service ticket
        service_ticket = ServiceTicket.query.get(ticket_id)
        if not service_ticket:
            return jsonify({"error": "Service ticket not found"}), 404

        # Add mechanics to the ticket
        for mechanic_id in add_ids:
            mechanic = Mechanics.query.get(mechanic_id)
            if mechanic and mechanic not in service_ticket.mechanics:
                service_ticket.mechanics.append(mechanic)

        # Remove mechanics from the ticket
        for mechanic_id in remove_ids:
            mechanic = Mechanics.query.get(mechanic_id)
            if mechanic and mechanic in service_ticket.mechanics:
                service_ticket.mechanics.remove(mechanic)

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            "message": "Mechanics updated successfully",
            "data": service_ticket_schema.dump(service_ticket)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET all service tickets
@service_tickets_bp.route("/", methods=["GET"])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)  # Cache the response for 60 seconds
def get_service_tickets():
    try:
        all_service_tickets = ServiceTicket.query.all()
        return jsonify(service_tickets_schema.dump(all_service_tickets)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET a single service ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)  # Cache the response for 60 seconds
def get_service_ticket(ticket_id):
    try:
        service_ticket = ServiceTicket.query.get(ticket_id)
        if not service_ticket:
            return jsonify({"message": "Service ticket not found"}), 404

        return jsonify(service_ticket_schema.dump(service_ticket)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET service tickets for the authenticated customer
@service_tickets_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    try:
        # Query service tickets for the authenticated customer
        service_tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()

        if not service_tickets:
            return jsonify({"message": "No service tickets found for this customer"}), 404

        # Serialize and return the service tickets
        return jsonify(service_tickets_schema.dump(service_tickets)), 200

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


# ROUTES — MECHANICS CRUD

# CREATE MECHANIC
@mechanics_bp.route("/", methods=["POST"])
@limiter.limit("5 per minute")  # Use limiter directly
def add_mechanic():
    try:
        data = request.get_json() or {}

        mechanic_obj = mechanic_schema.load(data)

        # Check for existing mechanic with the same name
        existing = Mechanics.query.filter_by(name=mechanic_obj.name).first()
        if existing:
            return jsonify({"error": "Mechanic with this name already exists"}), 409

        db.session.add(mechanic_obj)
        db.session.commit()

        return jsonify({
            "message": "Mechanic added successfully",
            "data": mechanic_schema.dump(mechanic_obj)
        }), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


print("ServiceTicket routes loaded")

def register_routes(app):
    print("register_routes function defined")
    # Example: Register blueprints or routes here
    from . import service_tickets_bp, mechanics_bp
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")