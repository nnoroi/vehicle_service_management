from flask import Blueprint, render_template
from app.services.dashboard_service import get_dashboard_summary
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    return "Mercedes Vehicle Service Management"


@dashboard_bp.route("/dashboard")
def dashboard():
    summary = get_dashboard_summary()
    return render_template(
        "dashboard.html",
        total_vehicles = summary["total_vehicles"],
        total_service_records = summary["total_service_records"],
        vehicles_needing_service = summary["vehicles_needing_service"]
    )
