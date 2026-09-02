import pytest
import sqlite3
from app.models.vehicle import Vehicle
from app.models.service_record import ServiceRecord

from app.services.vehicle_service import create_vehicle
from app.services.service_record_service import (
    create_service_record,
    get_records_by_vehicle_id,
    get_all_records,
    update_service_record,
    delete_service_record,
    get_service_record_by_id
)


def test_create_service_record(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection", test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection", test_database
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
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Completed",
        notes="Oil and filter replaced"
    )
    created_record = create_service_record(record)

    assert created_record.id is not None
    assert created_record.vehicle_id == created_vehicle.id
    assert created_record.service_type == "Oil Change"
    assert created_record.cost == 75.00
    assert created_record.status == "Completed"


def test_get_records_by_vehicle_id(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection", test_database
    )
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection", test_database
    )
    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="E 53 AMG",
        year=2025,
        registration="MB25 XYZ",
        vin="W1K22222222222222",
        mileage=10000,
        fuel_type="Petrol"
    )

    created_vehicle = create_vehicle(vehicle)

    record = ServiceRecord(
        record_id=None,
        vehicle_id=created_vehicle.id,
        service_type="Oil Change",
        service_date="31/08/2026",
        mileage=10000,
        cost=75.00,
        status="Completed",
        notes="Oil and filter replaced"
    )

    create_service_record(record)

    records = get_records_by_vehicle_id(created_vehicle.id)

    assert len(records) == 1
    assert records[0].vehicle_id == created_vehicle.id
    assert records[0].service_type == "Oil Change"
    assert records[0].status == "Completed"


def test_get_all_records(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
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

    created_vehicle1 = create_vehicle(vehicle1)
    created_vehicle2 = create_vehicle(vehicle2)

    record1 = ServiceRecord(
        record_id=None,
        vehicle_id=created_vehicle1.id,
        service_type="Oil Change",
        service_date="31/08/2026",
        mileage=15000,
        cost=75.00,
        status="Completed",
        notes="Oil and filter replaced"
    )

    record2 = ServiceRecord(
        record_id=None,
        vehicle_id=created_vehicle2.id,
        service_type="Brake Inspection",
        service_date="30/08/2026",
        mileage=10000,
        cost=120.00,
        status="Completed",
        notes="Brakes inspected"
    )

    create_service_record(record1)
    create_service_record(record2)

    records = get_all_records()

    assert len(records) == 2
    assert records[0].service_type == "Oil Change"
    assert records[1].service_type == "Brake Inspection"


def test_update_service_record(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
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
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Scheduled",
        notes="Oil and filter replacement"
    )

    created_record = create_service_record(record)

    created_record.status = "Completed"
    created_record.cost = 95.00
    created_record.notes = "Oil and filter replaced."

    result = update_service_record(created_record)

    assert result is True
    records = get_records_by_vehicle_id(created_vehicle.id)

    assert records[0].status == "Completed"
    assert records[0].cost == 95.00
    assert records[0].notes == "Oil and filter replaced."


def test_delete_service_record(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
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
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Scheduled",
        notes="Oil and filter replacement"
    )

    created_record = create_service_record(record)
    result = delete_service_record(created_record.id)

    assert result is True
    records = get_records_by_vehicle_id(created_vehicle.id)
    assert len(records) == 0


def test_create_service_record_with_invalid_data(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    record = ServiceRecord(
        record_id=None,
        vehicle_id=9999,
        service_type="Oil Change",
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Scheduled",
        notes="Oil and filter replacement"
    )

    with pytest.raises(ValueError):
        create_service_record(record)


def test_create_service_record_with_negative_cost(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
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
        service_date="31/08/2026",
        mileage=18500,
        cost=-75.00,
        status="Scheduled",
        notes="Oil and filter replacement"
    )

    with pytest.raises(ValueError):
        create_service_record(record)


def test_create_service_record_with_negative_mileage(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
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
        service_date="31/08/2026",
        mileage=-18500,
        cost=75.00,
        status="Scheduled",
        notes="Oil and filter replacement"
    )

    with pytest.raises(ValueError):
        create_service_record(record)


def test_create_service_record_with_invalid_status(
    test_database,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
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
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Random",
        notes="Oil and filter replacement"
    )

    with pytest.raises(ValueError):
        create_service_record(record)


def test_update_nonexistent_service_record(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    record = ServiceRecord(
        record_id=9999,
        vehicle_id=1,
        service_type="Oil Change",
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Completed",
        notes="Oil and filter replaced"
    )

    result = update_service_record(record)

    assert result is False


def test_delete_nonexistent_service_record(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    result = delete_service_record(9999)

    assert result is False


def test_update_service_record_with_negative_cost(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="E 53 AMG",
        year=2025,
        registration="MB25 XYZ",
        vin="W1K22222222222222",
        mileage=10000,
        fuel_type="Petrol"
    )

    created_vehicle = create_vehicle(vehicle)

    record = ServiceRecord(
        record_id=None,
        vehicle_id=created_vehicle.id,
        service_type="Oil Change",
        service_date="31/08/2026",
        mileage=10000,
        cost=100.00,
        status="Scheduled",
        notes="Oil and filter replacement"
    )

    created_record = create_service_record(record)

    created_record.cost = -50.00

    with pytest.raises(ValueError):
        update_service_record(created_record)


def test_update_service_record_with_negative_mileage(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    vehicle = Vehicle(
        vehicle_id=None,
        make="Mercedes-Benz",
        model="E 53 AMG",
        year=2025,
        registration="MB25 XYZ",
        vin="W1K22222222222222",
        mileage=10000,
        fuel_type="Petrol"
    )

    created_vehicle = create_vehicle(vehicle)

    record = ServiceRecord(
        record_id=None,
        vehicle_id=created_vehicle.id,
        service_type="Oil Change",
        service_date="31/08/2026",
        mileage=10000,
        cost=100.00,
        status="Scheduled",
        notes="Oil and filter replacement"
    )

    created_record = create_service_record(record)

    created_record.mileage = -100

    with pytest.raises(ValueError):
        update_service_record(created_record)


def test_get_service_record_by_id(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
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
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Completed",
        notes="Oil and filter replaced"
    )

    created_record = create_service_record(record)

    result = get_service_record_by_id(created_record.id)

    assert result is not None
    assert result.id == created_record.id
    assert result.vehicle_id == created_vehicle.id
    assert result.service_type == "Oil Change"


def test_get_service_record_by_id_not_found(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    result = get_service_record_by_id(9999)
    assert result is None
