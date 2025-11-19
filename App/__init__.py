from flask import Flask
from App.extensions import db, ma
from App.config import DevelopmentConfig
from App.Blueprints.Service_Ticket_blueprint.routes import service_tickets_bp
from App.Blueprints.Mechanic_blueprint.routes import mechanics_bp
from App.Blueprints.Members_blueprint.routes import customers_bp


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/tickets")


    return app