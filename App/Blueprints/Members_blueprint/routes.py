from flask import request, jsonify, Flask
from flask import current_app as app
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from App.models import Customer
from App.extensions import db
from . import customers_bp

from.schemas import customers_schema, customer_schema



# ROUTES — CUSTOMERS CRUD

# CREATE CUSTOMER
@customers_bp.route("/customers", methods=["POST"])
def add_customer():
    try:
        data = request.get_json() or {}

        customer_obj = customer_schema.load(data)

        # Check for existing email
        existing = Customer.query.filter_by(email=customer_obj.email).first()
        if existing:
            return jsonify({"error": "Customer with this email already exists"}), 409

        db.session.add(customer_obj)
        db.session.commit()

        return jsonify({
            "message": "Customer added successfully",
            "data": customer_schema.dump(customer_obj)
        }), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET all customers
@customers_bp.route("/customers", methods=["GET"])
def get_customers():
    try:
        all_customers = Customer.query.all()
        return jsonify(customers_schema.dump(all_customers)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET a single customer
@customers_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"message": "Customer not found"}), 404

        return jsonify(customer_schema.dump(customer)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE customer
@customers_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"message": "Customer not found"}), 404

        db.session.delete(customer)
        db.session.commit()

        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update customer
@customers_bp.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    try:
        # Parse the request data
        data = request.get_json()

        # Fetch the customer by ID
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        # Update fields
        for key, value in data.items():
            if hasattr(customer, key):
                setattr(customer, key, value)

        db.session.commit()

        return jsonify({
            "message": "Customer updated successfully",
            "data": customer_schema.dump(customer)
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
@customers_bp.route("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}, 200


print("App.routes loaded")

def register_routes(app):
    print("register_routes function defined")
    # Example: Register blueprints or routes here
    from . import customers_bp
    app.register_blueprint(customers_bp, url_prefix="/customers")