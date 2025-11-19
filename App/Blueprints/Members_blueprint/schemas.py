from App.extensions import ma
from App.models import Customer, Cars, ServiceTicket, Mechanics
from marshmallow import Schema, fields

# SCHEMAS

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True


class CarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cars
        include_relationships = True
        load_instance = True


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


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
