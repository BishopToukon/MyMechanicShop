from App.extensions import ma
from App.models import Customer, ServiceTicket, Mechanics
from marshmallow import Schema, fields

# SCHEMAS

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True
        exclude = ("password_hash",)  # Exclude password_hash from serialization

    # Add a password field for input validation
    password = fields.String(load_only=True)


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_relationships = True
        load_instance = True


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        include_relationships = True
        load_instance = True
        
class LoginSchema(Schema):
        email = fields.Email(required=True)
        password_hash_hash = fields.String(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()