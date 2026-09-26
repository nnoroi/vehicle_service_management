from flask import Flask
from app.routes.dashboard_routes import dashboard_bp
from app.routes.vehicle_routes import vehicle_bp
from app.routes.service_routes import service_bp
from app.errors import register_error_handlers
from app.utils.date_utils import format_date_for_display


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)

    app.jinja_env.filters["uk_date"] = format_date_for_display

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(service_bp)
    register_error_handlers(app)

    return app
