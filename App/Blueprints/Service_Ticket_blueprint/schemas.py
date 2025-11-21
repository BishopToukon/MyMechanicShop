from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from App.extensions import ma, db
from App.models import ServiceTicket, Mechanics
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_relationships = True
        load_instance = True

    # Explicitly include the customer_id field for input validation
    customer_id = fields.Integer(required=True)

    # Exclude the customer relationship from input validation
    customer = ma.auto_field(dump_only=True)

class ServiceMechanicSchema(ma.SQLAlchemyAutoSchema):  # Renamed to avoid conflict
    class Meta:
        model = Mechanics
        include_relationships = True
        load_instance = True

mechanic_schema = ServiceMechanicSchema()
mechanics_schema = ServiceMechanicSchema(many=True)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)



