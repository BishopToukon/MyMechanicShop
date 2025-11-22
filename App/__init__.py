from flask import Flask, app
import os  # Import the os module
from App.Blueprints.Inventory.routes import inventory_bp  # Import the inventory blueprint
from App.extensions import db, ma, limiter, cache
from App.config import DevelopmentConfig, ProductionConfig
from App.Blueprints.Service_Ticket_blueprint.routes import service_tickets_bp
from App.Blueprints.Mechanic_blueprint.routes import mechanics_bp
from App.Blueprints.Members_blueprint.routes import customers_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

def create_app(config_name):
    app = Flask(__name__)
    if os.environ.get("RENDER") == "true":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")  # Register inventory blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)  # Registering our swagger blueprint

    return app

app = create_app('ProductionConfig')