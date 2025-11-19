from flask import Blueprint

service_ticket_bp = Blueprint('service_ticket_bp', __name__, url_prefix="/tickets")

from . import routes