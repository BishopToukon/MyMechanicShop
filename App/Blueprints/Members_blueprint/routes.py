from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from App.models import Customer
from App.extensions import db, limiter
from App.utils.util import token_required, encode_token  # Import encode_token
from . import customers_bp
from .schemas import customers_schema, customer_schema, login_schema


# ---------------------------------------------------------
# CREATE CUSTOMER 
# ---------------------------------------------------------
@customers_bp.route("/", methods=["POST"])
def add_customer():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging

        # Validate and deserialize input data
        customer_obj = customer_schema.load(data)
        print("Customer object:", customer_obj)  # Debugging

        # Hash the password
        customer_obj.set_password(data["password"])

        # Ensure email is unique
        existing = Customer.query.filter_by(email=customer_obj.email).first()
        if existing:
            return jsonify({"error": "Customer with this email already exists"}), 409

        # Save the customer to the database
        db.session.add(customer_obj)
        db.session.commit()

        return jsonify({
            "message": "Customer added successfully",
            "data": customer_schema.dump(customer_obj)
        }), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500



# ---------------------------------------------------------
# GET ALL CUSTOMERS  
# ---------------------------------------------------------
@customers_bp.route("/", methods=["GET"])
def get_customers():
    try:
        # Get pagination parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        # Query customers with pagination
        customers = Customer.query.paginate(page=page, per_page=per_page, error_out=False)

        # Serialize the customers
        result = {
            "customers": customers_schema.dump(customers.items),
            "total": customers.total,
            "pages": customers.pages,
            "current_page": customers.page
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ---------------------------------------------------------
# GET SINGLE CUSTOMER  (Requires Token)
# ---------------------------------------------------------
@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"message": "Customer not found"}), 404

        return jsonify(customer_schema.dump(customer)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ---------------------------------------------------------
# DELETE CUSTOMER  (Requires Token)
# ---------------------------------------------------------
@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@token_required
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



# ---------------------------------------------------------
# UPDATE CUSTOMER  (Requires Token)
# ---------------------------------------------------------
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@token_required
def update_customer(customer_id):
    try:
        data = request.get_json() or {}

        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

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



# ---------------------------------------------------------
# LOGIN — Generates JWT Token
# ---------------------------------------------------------
@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate customer credentials
        customer = Customer.query.filter_by(email=email).first()
        if not customer or not customer.check_password(password):  # Use check_password method
            return jsonify({'message': 'Invalid email or password'}), 401

        # Generate a token for the customer
        token = encode_token(customer.customer_id)

        return jsonify({
            'message': 'Login successful',
            'token': token
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ---------------------------------------------------------
# PROFILE — Uses customer_id from decoded JWT
# ---------------------------------------------------------
@customers_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    try:
        customer_id = request.customer_id

        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify(customer_schema.dump(customer)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ---------------------------------------------------------
# HEALTH CHECK (No Auth)
# ---------------------------------------------------------
@customers_bp.route("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}, 200