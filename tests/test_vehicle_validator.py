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


def test_valid_vehicle_with_minimum_year():
    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="190E",
        year=1886,
        registration="MB86 XYZ",
        vin="WDB20100000000001",
        mileage=0,
        fuel_type="Petrol"
    )
    errors = validate_vehicle(vehicle)
    assert errors == []


def test_valid_vehicle_with_zero_mileage():
    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="E 300",
        year=2025,
        registration="MB25 ZERO",
        vin="W1K33333333333333",
        mileage=0,
        fuel_type="Diesel"
    )

    errors = validate_vehicle(vehicle)

    assert errors == []


def test_invalid_vehicle_year_type():
    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="AMG C 63",
        year="2024",
        registration="MB24 XYZ",
        vin="W1K98765432109876",
        mileage=18500,
        fuel_type="Petrol"
    )

    errors = validate_vehicle(vehicle)
    assert "Year must be a number." in errors
