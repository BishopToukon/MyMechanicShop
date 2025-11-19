from App.models import Customer, Mechanics, ServiceTicket  # Import your models
from App.schemas import Customers_schema, Customer_schema, Mechanics_schema, Mechanic_schema, ServiceTickets_schema, ServiceTicket_schema  # Import your schemas
from flask import request
from .extensions import SQLAlchemy
from App.extensions import db  # Import the database instance

def register_routes(app):
    # Home route
    @app.route("/")
    def home():
        return "Welcome to My Mechanic Shop!"

    # Customers routes
    @app.route("/customers", methods=["GET"])
    def get_customers():
        try:
            # Query all customers from the database
            all_customers = Customer.query.all()

            # Serialize the data using Marshmallow schema
            result = Customers_schema.dump(all_customers)

            return {"customers": result}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    @app.route("/customers/<int:customer_id>", methods=["GET"])
    def get_customer(customer_id):
        try:
            # Query a specific customer by ID
            customer = Customer.query.get(customer_id)

            if not customer:
                return {"error": "Customer not found"}, 404

            # Serialize the data using Marshmallow schema
            result = Customer_schema.dump(customer)

            return {"customer": result}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    @app.route("/customers", methods=["POST"])
    def add_customer():
        try:
            # Parse the request JSON
            data = request.get_json()

            # Create a new customer object
            new_customer = Customer(
                name=data["name"],
                address=data["address"],
                email=data["email"],
                phone=data["phone"]
            )

            # Add the new customer to the database
            db.session.add(new_customer)
            db.session.commit()

            # Serialize the new customer
            result = Customer_schema.dump(new_customer)

            return {"message": "Customer added successfully", "customer": result}, 201
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    @app.route("/customers/<int:customer_id>", methods=["PUT"])
    def update_customer(customer_id):
        try:
            # Query the customer by ID
            customer = Customer.query.get(customer_id)

            if not customer:
                return {"error": "Customer not found"}, 404

            # Parse the request JSON
            data = request.get_json()

            # Update the customer's fields
            customer.name = data.get("name", customer.name)
            customer.address = data.get("address", customer.address)
            customer.email = data.get("email", customer.email)
            customer.phone = data.get("phone", customer.phone)

            # Commit the changes to the database
            db.session.commit()

            # Serialize the updated customer
            result = Customer_schema.dump(customer)

            return {"message": "Customer updated successfully", "customer": result}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    @app.route("/customers/<int:customer_id>", methods=["DELETE"])
    def delete_customer(customer_id):
        try:
            # Query the customer by ID
            customer = Customer.query.get(customer_id)

            if not customer:
                return {"error": "Customer not found"}, 404

            # Delete the customer from the database
            db.session.delete(customer)
            db.session.commit()

            return {"message": f"Customer {customer_id} deleted successfully"}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    # Mechanics routes
    @app.route("/mechanics", methods=["GET"])
    def get_mechanics():
        try:
            # Query all mechanics from the database
            all_mechanics = Mechanics.query.all()

            # Serialize the data using Marshmallow schema
            result = Mechanics_schema.dump(all_mechanics)

            return {"mechanics": result}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    @app.route("/mechanics/<int:mechanic_id>", methods=["GET"])
    def get_mechanic(mechanic_id):
        try:
            # Query a specific mechanic by ID
            mechanic = Mechanics.query.get(mechanic_id)

            if not mechanic:
                return {"error": "Mechanic not found"}, 404

            # Serialize the data using Marshmallow schema
            result = Mechanic_schema.dump(mechanic)

            return {"mechanic": result}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    # Service Tickets routes
    @app.route("/service_tickets", methods=["GET"])
    def get_service_tickets():
        try:
            # Query all service tickets from the database
            all_tickets = ServiceTicket.query.all()

            # Serialize the data using Marshmallow schema
            result = ServiceTickets_schema.dump(all_tickets)

            return {"service_tickets": result}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500

    @app.route("/service_tickets/<int:ticket_id>", methods=["GET"])
    def get_service_ticket(ticket_id):
        try:
            # Query a specific service ticket by ID
            ticket = ServiceTicket.query.get(ticket_id)

            if not ticket:
                return {"error": "Service ticket not found"}, 404

            # Serialize the data using Marshmallow schema
            result = ServiceTicket_schema.dump(ticket)

            return {"service_ticket": result}, 200
        except Exception as e:
            # Handle unexpected errors
            return {"error": str(e)}, 500