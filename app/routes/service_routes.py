from flask import Blueprint, jsonify, request, render_template, redirect
from app.models.service_record import ServiceRecord
from app.services.service_record_mapper import service_record_to_dict
from app.services.service_record_service import (
    get_records_by_vehicle_id,
    get_service_record_by_id,
    create_service_record,
    update_service_record,
    delete_service_record,
    get_all_records
)
from app.services.vehicle_service import get_vehicle_by_id


service_bp = Blueprint("services", __name__)


@service_bp.route("/services")
def get_services():
    records = get_all_records()

    vehicles = {}
    for record in records:
        vehicles[record.vehicle_id] = get_vehicle_by_id(record.vehicle_id)

    return render_template(
        "services/list.html",
        records=records,
        vehicles=vehicles
    )


@service_bp.route("/vehicles/<int:vehicle_id>/services")
def get_vehicle_services(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return jsonify({
            "error": "Vehicle not found."
        }), 404

    records = get_records_by_vehicle_id(vehicle_id)

    return jsonify([
        service_record_to_dict(record)
        for record in records
    ])


@service_bp.route("/vehicles/<int:vehicle_id>/services", methods=["POST"])
def create_vehicle_service(vehicle_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return jsonify({
            "error": "Vehicle not found."
        }), 404

    requested_fields = [
        "service_type",
        "service_date",
        "mileage",
        "cost",
        "status"
    ]

    missing_fields = [
        field
        for field in requested_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    service_record = ServiceRecord(
        vehicle_id=vehicle_id,
        service_type=data["service_type"],
        service_date=data["service_date"],
        mileage=data["mileage"],
        cost=data["cost"],
        status=data["status"],
        notes=data.get("notes")
    )

    service_record = create_service_record(service_record)

    return jsonify(service_record_to_dict(service_record)), 201


@service_bp.route("/vehicles/<int:vehicle_id>/services/new", methods=["GET"])
def new_service(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return "Vehicle not found", 404

    return render_template(
        "services/create.html",
        vehicle=vehicle
    )


@service_bp.route("/vehicles/<int:vehicle_id>/services/new", methods=["POST"])
def submit_new_service(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return "Vehicle not found", 404

    record = ServiceRecord(
        vehicle_id=vehicle_id,
        service_type=request.form["service_type"],
        service_date=request.form["service_date"],
        mileage=int(request.form["mileage"]),
        cost=float(request.form["cost"]),
        status=request.form["status"],
        notes=request.form.get("notes")
    )

    try:
        create_service_record(record)
    except ValueError as error:
        return render_template(
            "services/create.html",
            vehicle=vehicle,
            error=str(error),
            record=record
        )

    return redirect(f"/services/{record.id}/details")


@service_bp.route("/services/<int:service_id>")
def get_service(service_id):
    record = get_service_record_by_id(service_id)

    if not record:
        return jsonify({
            "error": "Service record not found."
        }), 404

    return jsonify(service_record_to_dict(record)), 200


@service_bp.route("/services/<int:service_id>/details")
def service_details(service_id):
    record = get_service_record_by_id(service_id)

    if not record:
        return "Service record not found", 404

    vehicle = get_vehicle_by_id(record.vehicle_id)

    return render_template(
        "services/details.html",
        record=record,
        vehicle=vehicle
    )


@service_bp.route("/services/<int:service_id>/edit", methods=["GET"])
def edit_service(service_id):
    record = get_service_record_by_id(service_id)

    if not record:
        return "Service record not found", 404

    vehicle = get_vehicle_by_id(record.vehicle_id)

    return render_template(
        "services/edit.html",
        record=record,
        vehicle=vehicle
    )


@service_bp.route("/services/<int:service_id>/edit", methods=["POST"])
def submit_edit_service(service_id):
    record = get_service_record_by_id(service_id)

    if not record:
        return "Service record not found", 404

    record.service_type = request.form["service_type"]
    record.service_date = request.form["service_date"]
    record.mileage = int(request.form["mileage"])
    record.cost = float(request.form["cost"])
    record.status = request.form["status"]
    record.notes = request.form.get("notes")

    try:
        update_service_record(record)
    except ValueError as error:
        vehicle = get_vehicle_by_id(record.vehicle_id)
        return render_template(
            "services/edit.html",
            record=record,
            vehicle=vehicle,
            error=str(error)
        )

    return redirect(f"/services/{service_id}/details")


@service_bp.route("/services/<int:service_id>/delete", methods=["POST"])
def submit_delete_service(service_id):
    deleted = delete_service_record(service_id)

    if not deleted:
        return "Service record not found", 404

    return redirect("/services")


@service_bp.route("/services/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    service_record = get_service_record_by_id(service_id)

    if not service_record:
        return jsonify({
            "error": "Service record not found."
        }), 404

    service_record.service_type = data.get(
        "service_type",
        service_record.service_type
    )

    service_record.service_date = data.get(
        "service_date",
        service_record.service_date
    )

    service_record.mileage = data.get(
        "mileage",
        service_record.mileage
    )

    service_record.cost = data.get(
        "cost",
        service_record.cost
    )

    service_record.status = data.get(
        "status",
        service_record.status
    )

    service_record.notes = data.get(
        "notes",
        service_record.notes
    )

    update_service_record(service_record)

    return jsonify(service_record_to_dict(service_record)), 200


@service_bp.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    deleted = delete_service_record(service_id)

    if not deleted:
        return jsonify({
            "error": "Service record not found."
        }), 404

    return jsonify({
        "message": "Service record deleted successfully."
    }), 200
