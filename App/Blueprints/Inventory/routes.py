from flask import request, jsonify, Blueprint
from App.models import Inventory
from App.extensions import db
from marshmallow.exceptions import ValidationError
from .schemas import inventory_schema, inventories_schema

# Define the Blueprint for inventory
inventory_bp = Blueprint('inventory', __name__)

# CREATE Inventory Item
@inventory_bp.route("/", methods=["POST"])
def create_inventory_item():
    try:
        data = request.get_json() or {}
        inventory_item = inventory_schema.load(data)

        # Add the inventory item to the database
        db.session.add(inventory_item)
        db.session.commit()

        return jsonify({
            "message": "Inventory item created successfully",
            "data": inventory_schema.dump(inventory_item)
        }), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        print("Error:", str(e))  # Log the error
        return jsonify({"error": str(e)}), 500


# READ All Inventory Items
@inventory_bp.route("/", methods=["GET"])
def get_all_inventory_items():
    try:
        inventory_items = Inventory.query.all()
        return jsonify(inventories_schema.dump(inventory_items)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# READ Single Inventory Item
@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    try:
        inventory_item = Inventory.query.get(item_id)
        if not inventory_item:
            return jsonify({"error": "Inventory item not found"}), 404

        return jsonify(inventory_schema.dump(inventory_item)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE Inventory Item
@inventory_bp.route("/<int:item_id>", methods=["PUT"])
def update_inventory_item(item_id):
    try:
        inventory_item = Inventory.query.get(item_id)
        if not inventory_item:
            return jsonify({"error": "Inventory item not found"}), 404

        data = request.get_json() or {}
        inventory_item = inventory_schema.load(data, instance=inventory_item, partial=True)

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            "message": "Inventory item updated successfully",
            "data": inventory_schema.dump(inventory_item)
        }), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE Inventory Item
@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    try:
        inventory_item = Inventory.query.get(item_id)
        if not inventory_item:
            return jsonify({"error": "Inventory item not found"}), 404

        # Delete the inventory item from the database
        db.session.delete(inventory_item)
        db.session.commit()

        return jsonify({"message": "Inventory item deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500