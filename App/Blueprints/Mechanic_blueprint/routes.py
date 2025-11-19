from flask import request, jsonify
from flask import current_app as app
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from App.models import Mechanics
from App.extensions import db
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


# ROUTES — MECHANICS CRUD

# CREATE MECHANIC
@mechanics_bp.route("/", methods=["POST"])
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


# GET all mechanics
@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    try:
        all_mechanics = Mechanics.query.all()
        return jsonify(mechanics_schema.dump(all_mechanics)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET a single mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    try:
        mechanic = Mechanics.query.get(mechanic_id)
        if not mechanic:
            return jsonify({"message": "Mechanic not found"}), 404

        return jsonify(mechanic_schema.dump(mechanic)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    try:
        mechanic = Mechanics.query.get(mechanic_id)
        if not mechanic:
            return jsonify({"message": "Mechanic not found"}), 404

        db.session.delete(mechanic)
        db.session.commit()

        return jsonify({"message": "Mechanic deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    try:
        # Parse the request data
        data = request.get_json()

        # Fetch the mechanic by ID
        mechanic = Mechanics.query.get(mechanic_id)
        if not mechanic:
            return jsonify({"error": "Mechanic not found"}), 404

        # Update fields
        for key, value in data.items():
            if hasattr(mechanic, key):
                setattr(mechanic, key, value)

        db.session.commit()

        return jsonify({
            "message": "Mechanic updated successfully",
            "data": mechanic_schema.dump(mechanic)
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
@mechanics_bp.route("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}, 200


print("Mechanic routes loaded")

def register_routes(app):
    print("register_routes function defined")
    # Example: Register blueprints or routes here
    from . import mechanics_bp
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")