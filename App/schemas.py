from App.extensions import ma
from App.models import Customer, ServiceTicket, Mechanics  # Ensure these models are defined in App.models

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True

Customers_schema = CustomerSchema(many=True)
Customer_schema = CustomerSchema()


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_relationships = True
        load_instance = True

ServiceTickets_schema = ServiceTicketSchema(many=True)
ServiceTicket_schema = ServiceTicketSchema()


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        include_relationships = True
        load_instance = True

Mechanics_schema = MechanicSchema(many=True)
Mechanic_schema = MechanicSchema()
