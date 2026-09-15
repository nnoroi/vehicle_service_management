from flask import Blueprint, render_template, request, jsonify, redirect
from app.models.vehicle import Vehicle
from app.services.maintenance_service import get_maintenance_status
from app.services.vehicle_service import (
    get_all_vehicles,
    get_vehicle_by_id,
    create_vehicle,
    update_vehicle,
    delete_vehicle
)
vehicle_bp = Blueprint("vehicles", __name__)


@vehicle_bp.route("/vehicles")
def get_vehicles():
    vehicles_list = get_all_vehicles()
    return render_template(
        "vehicles/list.html",
        vehicles = vehicles_list
    )

@vehicle_bp.route("/vehicles/add", methods=["GET", "POST"])
def add_vehicle():
    if request.method == "POST":
        vehicle = Vehicle(
            make=request.form["make"],
            model=request.form["model"],
            year=int(request.form["year"]),
            registration=request.form["registration"],
            vin=request.form["vin"],
            mileage=int(request.form["mileage"]),
            fuel_type=request.form["fuel_type"]
        )

        try:
            vehicle = create_vehicle(vehicle)
        except ValueError as error:
            return render_template(
                "vehicles/add.html",
                error = str(error),
                vehicle = vehicle
            ), 400

        return redirect(f"/vehicles/{vehicle.id}")
    return render_template("vehicles/add.html")


@vehicle_bp.route("/vehicles/<int:vehicle_id>")
def get_vehicle(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    
    if not vehicle:
        return "Vehicle not found", 404

    return render_template(
        "vehicles/details.html",
        vehicle = vehicle
    )

    return jsonify({"error": "Vehicle not found"}), 404


@vehicle_bp.route("/vehicles", methods=["POST"])
def create_vehicle_route():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400
    requested_fields = [
        "make",
        "model",
        "year",
        "registration",
        "mileage",
        "fuel_type"
    ]
    missing_fields = [
        field for field in requested_fields
        if field not in data
    ]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    vehicle = Vehicle(
        make=data["make"],
        model=data["model"],
        year=data["year"],
        registration=data["registration"],
        vin=data.get("vin"),
        mileage=data["mileage"],
        fuel_type=data["fuel_type"]
    )
    try:
        vehicle = create_vehicle(vehicle)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "registration": vehicle.registration,
        "vin": vehicle.vin,
        "mileage": vehicle.mileage,
        "fuel_type": vehicle.fuel_type
    }), 201


@vehicle_bp.route("/vehicles/<int:vehicle_id>", methods=["PUT"])
def update_vehicle_route(vehicle_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return jsonify({
            "error": "Vehicle not found"
        }), 404

    vehicle.make = data.get("make", vehicle.make)
    vehicle.model = data.get("model", vehicle.model)
    vehicle.year = data.get("year", vehicle.year)
    vehicle.registration = data.get("registration", vehicle.registration)
    vehicle.vin = data.get("vin", vehicle.vin)
    vehicle.mileage = data.get("mileage", vehicle.mileage)
    vehicle.fuel_type = data.get("fuel_type", vehicle.fuel_type)

    try:
        update_vehicle(vehicle)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "registration": vehicle.registration,
        "vin": vehicle.vin,
        "mileage": vehicle.mileage,
        "fuel_type": vehicle.fuel_type
    }), 200


@vehicle_bp.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle_route(vehicle_id):
    deleted = delete_vehicle(vehicle_id)

    if not deleted:
        return jsonify({
            "error": "Vehicle not found."
        }), 404

    return jsonify({
        "message": "Vehicle deleted successfully."
    }), 200


@vehicle_bp.route("/vehicles/<int:vehicle_id>/maintenance")
def get_vehicle_maintenance(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return jsonify({
            "error": "Vehicle not found."
        }), 404

    maintenance_status = get_maintenance_status(vehicle_id, vehicle.mileage)
    return jsonify(maintenance_status), 200
