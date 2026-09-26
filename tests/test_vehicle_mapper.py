from app.models.vehicle import Vehicle
from app.services.vehicle_mapper import (
    row_to_vehicle,
    vehicle_to_dict
)


def test_row_to_vehicle():
    row = {
        "id": 1,
        "make": "Mercedes-Benz",
        "model": "E-Class",
        "year": 2025,
        "registration": "MB25 ECL",
        "vin": "W1K12345678901234",
        "mileage": 40000,
        "fuel_type": "Diesel"
    }

    vehicle = row_to_vehicle(row)

    assert vehicle.id == 1
    assert vehicle.make == "Mercedes-Benz"
    assert vehicle.model == "E-Class"
    assert vehicle.year == 2025
    assert vehicle.registration == "MB25 ECL"
    assert vehicle.vin == "W1K12345678901234"
    assert vehicle.mileage == 40000
    assert vehicle.fuel_type == "Diesel"


def test_vehicle_to_dict():
    vehicle = Vehicle(
        vehicle_id=1,
        make="Mercedes-Benz",
        model="E-Class",
        year=2025,
        registration="MB25 ECL",
        vin="W1K12345678901234",
        mileage=40000,
        fuel_type="Diesel"
    )

    result = vehicle_to_dict(vehicle)

    assert result == {
        "id": 1,
        "make": "Mercedes-Benz",
        "model": "E-Class",
        "year": 2025,
        "registration": "MB25 ECL",
        "vin": "W1K12345678901234",
        "mileage": 40000,
        "fuel_type": "Diesel"
    }
