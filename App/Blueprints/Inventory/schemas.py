from App.models import Inventory, Customer, ServiceTicket, Mechanics
from App.extensions import ma

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
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

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory  # Link the schema to the Inventory model
        include_relationships = True  # Include relationships if any
        load_instance = True  # Deserialize to model instances

# Single inventory item schema
inventory_schema = InventorySchema()

# Multiple inventory items schema
inventories_schema = InventorySchema(many=True)