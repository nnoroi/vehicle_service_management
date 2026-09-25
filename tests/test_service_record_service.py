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

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
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

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
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
    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
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

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
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

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
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


def test_get_service_history_summary(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    connection = test_database()
    connection.execute(
        """
        INSERT INTO vehicles (
            make,
            model,
            year,
            registration,
            vin,
            mileage,
            fuel_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "C 300",
            2022,
            "MJ22 XTR",
            "W1K2060421F123456",
            40000,
            "Petrol"
        )
    )

    vehicle_id = connection.execute(
        "SELECT id FROM vehicles WHERE registration = ?",
        ("MJ22 XTR",)
    ).fetchone()["id"]

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Oil Change",
            "2026-03-10",
            30000,
            120.00,
            "Completed",
            "Oil and filter replaced"
        )
    )

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-09-15",
            40000,
            600.00,
            "Completed",
            "Full Mercedes service completed"
        )
    )

    connection.commit()

    from app.services.service_record_service import get_service_history_summary

    summary = get_service_history_summary(vehicle_id)

    assert summary["total_services"] == 2
    assert summary["last_service_date"] == "2026-09-15"
    assert summary["last_service_mileage"] == 40000
    assert summary["total_cost"] == 720.00


def test_get_service_history_summary_uses_latest_service_mileage(
    test_database,
    monkeypatch
):

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    connection = test_database()

    connection.execute(
        """
        INSERT INTO vehicles (
            make,
            model,
            year,
            registration,
            vin,
            mileage,
            fuel_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "E-Class",
            2025,
            "MB25 ECL",
            "W1K12345678901234",
            40000,
            "Diesel"
        )
    )

    vehicle_id = connection.execute(
        "SELECT id FROM vehicles WHERE registration = ?",
        ("MB25 ECL",)
    ).fetchone()["id"]

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-06-15",
            35000,
            500.00,
            "Completed",
            "Full service"
        )
    )

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Brake Service",
            "2026-09-15",
            25000,
            300.00,
            "Completed",
            "Brake inspection"
        )
    )

    connection.commit()

    from app.services.service_record_service import get_service_history_summary

    summary = get_service_history_summary(vehicle_id)

    assert summary["last_service_date"] == "2026-09-15"
    assert summary["last_service_mileage"] == 25000


def test_get_service_history_summary_empty(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    connection = test_database()

    connection.execute(
        """
        INSERT INTO vehicles (
            make,
            model,
            year,
            registration,
            vin,
            mileage,
            fuel_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "S-Class",
            2024,
            "MS24 ABC",
            "W1K98765432101234",
            10000,
            "Petrol"
        )
    )

    vehicle_id = connection.execute(
        "SELECT id FROM vehicles WHERE registration = ?",
        ("MS24 ABC",)
    ).fetchone()["id"]

    connection.commit()

    from app.services.service_record_service import get_service_history_summary

    summary = get_service_history_summary(vehicle_id)

    assert summary["total_services"] == 0
    assert summary["last_service_date"] is None
    assert summary["last_service_mileage"] is None
    assert summary["total_cost"] == 0


def test_create_service_record_rejects_lower_mileage(
    test_database,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_vehicle_by_id",
        lambda vehicle_id: Vehicle(
            vehicle_id=vehicle_id,
            make="Mercedes-Benz",
            model="E-Class",
            year=2025,
            registration="MB25 ECL",
            vin="W1K12345678901234",
            mileage=40000,
            fuel_type="Diesel"
        )
    )

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    connection = test_database()

    connection.execute(
        """
        INSERT INTO vehicles (
            make,
            model,
            year,
            registration,
            vin,
            mileage,
            fuel_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "E-Class",
            2025,
            "MB25 ECL",
            "W1K12345678901234",
            40000,
            "Diesel"
        )
    )

    vehicle_id = connection.execute(
        "SELECT id FROM vehicles WHERE registration = ?",
        ("MB25 ECL",)
    ).fetchone()["id"]

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-06-15",
            35000,
            500.00,
            "Completed",
            "Full service"
        )
    )

    connection.commit()

    record = ServiceRecord(
        vehicle_id=vehicle_id,
        service_type="Brake Service",
        service_date="2026-09-15",
        mileage=30000,
        cost=300.00,
        status="Completed",
        notes="Brake inspection"
    )

    with pytest.raises(ValueError, match="previous service mileage"):
        create_service_record(record)


def test_update_service_record_rejects_lower_mileage(
    test_database,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.service_record_service.get_vehicle_by_id",
        lambda vehicle_id: Vehicle(
            vehicle_id=vehicle_id,
            make="Mercedes-Benz",
            model="E-Class",
            year=2025,
            registration="MB25 ECL",
            vin="W1K12345678901234",
            mileage=40000,
            fuel_type="Diesel"
        )
    )

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    connection = test_database()

    connection.execute(
        """
        INSERT INTO vehicles (
            make,
            model,
            year,
            registration,
            vin,
            mileage,
            fuel_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "E-Class",
            2025,
            "MB25 ECL",
            "W1K12345678901234",
            40000,
            "Diesel"
        )
    )

    vehicle_id = connection.execute(
        "SELECT id FROM vehicles WHERE registration = ?",
        ("MB25 ECL",)
    ).fetchone()["id"]

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-06-15",
            35000,
            500.00,
            "Completed",
            "Full service"
        )
    )

    second_record = connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Oil Change",
            "2026-09-15",
            40000,
            200.00,
            "Completed",
            "Oil change"
        )
    )

    connection.commit()

    second_record_id = second_record.lastrowid
    connection.close()

    record = ServiceRecord(
        vehicle_id=vehicle_id,
        service_type="Oil Change",
        service_date="2026-09-15",
        mileage=30000,
        cost=200.00,
        status="Completed",
        notes="Updated oil change",
        record_id=second_record_id
    )

    with pytest.raises(ValueError, match="previous service mileage"):
        update_service_record(record)


def test_update_service_record_rejects_higher_than_next_mileage(
    test_database,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    connection = test_database()

    cursor = connection.execute(
        """
        INSERT INTO vehicles (
            make,
            model,
            year,
            registration,
            vin,
            mileage,
            fuel_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "E-Class",
            2025,
            "MB25 ECL",
            "W1K12345678901234",
            45000,
            "Diesel"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-06-15",
            35000,
            500.00,
            "Completed",
            "Full service"
        )
    )

    cursor = connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Oil Change",
            "2026-09-15",
            40000,
            200.00,
            "Completed",
            "Oil change"
        )
    )

    service_id = cursor.lastrowid

    connection.execute(
        """
        INSERT INTO service_records (
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Brake Service",
            "2026-12-15",
            45000,
            300.00,
            "Completed",
            "Brake inspection"
        )
    )

    connection.commit()
    connection.close()

    record = ServiceRecord(
        vehicle_id=vehicle_id,
        service_type="Oil Change",
        service_date="2026-09-15",
        mileage=50000,
        cost=200.00,
        status="Completed",
        notes="Updated oil change",
        record_id=service_id
    )

    with pytest.raises(ValueError, match="next service mileage"):
        update_service_record(record)
