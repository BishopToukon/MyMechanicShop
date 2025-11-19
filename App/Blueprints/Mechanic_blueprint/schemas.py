from App.extensions import ma
from App.models import Customer, Cars, ServiceTicket, Mechanics
from App.models import Mechanics

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


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
