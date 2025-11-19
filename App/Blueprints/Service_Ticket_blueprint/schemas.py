from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from App.extensions import ma, db
from App.models import ServiceTicket

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session
        include_fk = True        # allow vin
        include_relationships = False  # <-- IMPORTANT FIX

    # Explicitly exclude relationship fields from input validation
    car = ma.auto_field(dump_only=True)
    mechanics = ma.auto_field(dump_only=True)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)



