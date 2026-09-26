import pytest
from app.models.vehicle import Vehicle
from app.models.service_record import ServiceRecord
from app.services.vehicle_service import (
    create_vehicle,
    get_all_vehicles,
    get_vehicle_by_id,
    update_vehicle,
    delete_vehicle
)

from app.services.service_record_service import (
    create_service_record,
    get_records_by_vehicle_id
)


def test_create_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection", test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="AMG C 63",
        year=2024,
        registration="MB24 XYZ",
        vin="W1K98765432109876",
        mileage=18500,
        fuel_type="Petrol"
    )
    created_vehicle = create_vehicle(vehicle)

    assert created_vehicle.id is not None
    assert created_vehicle.make == "Mercedes-Benz"
    assert created_vehicle.model == "AMG C 63"


def test_get_vehicle_by_id(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection", test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="S-Class",
        year=2025,
        registration="AB22 ABC",
        vin="JTDB12345678901234",
        mileage=30000,
        fuel_type="Petrol"
    )

    created_vehicle = create_vehicle(vehicle)
    retrieved_vehicle = get_vehicle_by_id(created_vehicle.id)

    assert retrieved_vehicle is not None
    assert retrieved_vehicle.id == created_vehicle.id
    assert retrieved_vehicle.make == "Mercedes-Benz"
    assert retrieved_vehicle.model == "S-Class"


def test_get_all_vehicles(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    vehicle1 = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="C 63 AMG",
        year=2024,
        registration="MB24 ABC",
        vin="W1K11111111111111",
        mileage=15000,
        fuel_type="Petrol"
    )

    vehicle2 = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="E 53 AMG",
        year=2025,
        registration="MB25 XYZ",
        vin="W1K22222222222222",
        mileage=10000,
        fuel_type="Petrol"
    )
    create_vehicle(vehicle1)
    create_vehicle(vehicle2)

    vehicles = get_all_vehicles()

    assert len(vehicles) == 2
    assert vehicles[0].model == "C 63 AMG"
    assert vehicles[1].model == "E 53 AMG"


def test_update_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection", test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="AMG C 63",
        year=2024,
        registration="MB24 XYZ",
        vin="W1K98765432109876",
        mileage=18500,
        fuel_type="Petrol"
    )

    created_vehicle = create_vehicle(vehicle)

    created_vehicle.mileage = 50000
    result = update_vehicle(created_vehicle)

    assert result is True
    updated_vehicle = get_vehicle_by_id(created_vehicle.id)
    assert updated_vehicle.mileage == 50000


def test_delete_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection", test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="AMG C 63",
        year=2024,
        registration="MB24 XYZ",
        vin="W1K98765432109876",
        mileage=18500,
        fuel_type="Petrol"
    )

    created_vehicle = create_vehicle(vehicle)

    result = delete_vehicle(created_vehicle.id)

    assert result is True
    assert get_vehicle_by_id(created_vehicle.id) is None


def test_delete_vehicle_cascades_service_records(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )
    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="AMG C 63",
        year=2024,
        registration="MB24 XYZ",
        vin="W1K98765432109876",
        mileage=18500,
        fuel_type="Petrol"
    )

    created_vehicle = create_vehicle(vehicle)

    record = ServiceRecord(
        record_id=None,
        vehicle_id=created_vehicle.id,
        service_type="Oil Change",
        service_date="2026-08-31",
        mileage=18500,
        cost=75.00,
        status="Completed",
        notes="Oil and filter replaced"
    )

    create_service_record(record)
    result = delete_vehicle(created_vehicle.id)
    assert result is True

    records = get_records_by_vehicle_id(created_vehicle.id)
    assert len(records) == 0


def test_create_vehicle_invalid_data(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="",
        model="AMG C 63",
        year=2024,
        registration="MB24 XYZ",
        vin="W1K98765432109876",
        mileage=18500,
        fuel_type="Petrol"
    )

    with pytest.raises(ValueError):
        create_vehicle(vehicle)


def test_update_vehicle_with_invalid_data(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="AMG C 63",
        year=2024,
        registration="MB24 XYZ",
        vin="W1K98765432109876",
        mileage=18500,
        fuel_type="Petrol"
    )
    created_vehicle = create_vehicle(vehicle)
    created_vehicle.make = ""

    with pytest.raises(ValueError):
        update_vehicle(created_vehicle)
