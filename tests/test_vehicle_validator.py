from app.models.vehicle import Vehicle
from app.validators.vehicle_validator import validate_vehicle


def test_valid_vehicles():
    vehicle = Vehicle(
        vehicle_id=None,
        make="BMW",
        model="M3",
        year=2023,
        registration="AB23 XYZ",
        vin="WBS12345678901234",
        mileage=18500,
        fuel_type="Petrol"
    )

    errors = validate_vehicle(vehicle)

    assert errors == []


def test_invalid_vehicle():
    vehicle = Vehicle(
        vehicle_id=None,
        make="",
        model="",
        year=1800,
        registration="",
        vin=None,
        mileage=-500,
        fuel_type=""
    )

    errors = validate_vehicle(vehicle)

    assert "Make is required." in errors
    assert "Model is required." in errors
    assert "Year must be a 1886 or later." in errors
    assert "Registration is required." in errors
    assert "Mileage cannot be negative." in errors
    assert "Fuel type is required." in errors
