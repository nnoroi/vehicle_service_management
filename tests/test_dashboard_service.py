from app import create_app
from app.services.dashboard_service import (
    get_total_vehicles,
    get_total_service_records,
    get_vehicles_needing_service,
    get_dashboard_summary
)


def test_get_total_vehicles(monkeypatch, test_database):
    monkeypatch.setattr(
        "app.services.dashboard_service.get_connection",
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
            "C-Class",
            2024,
            "MB24 CCL",
            "WDD12345678901231",
            15000,
            "Petrol"
        )
    )

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
            "WDD12345678901232",
            10000,
            "Diesel"
        )
    )

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
            2025,
            "MB25 SCL",
            "WDD12345678901235",
            5000,
            "Petrol"
        )
    )

    connection.commit()
    connection.close()

    total_vehicles = get_total_vehicles()

    assert total_vehicles == 3


def test_get_total_service_records(monkeypatch, test_database):
    monkeypatch.setattr(
        "app.services.dashboard_service.get_connection",
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
            "C-Class",
            2024,
            "MB24 CCL",
            "WDD12345678901231",
            15000,
            "Petrol"
        )
    )

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
            "WDD12345678901232",
            10000,
            "Diesel"
        )
    )

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
            2025,
            "MB25 SCL",
            "WDD12345678901235",
            5000,
            "Petrol"
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
            1,
            "Oil Change",
            "2026-06-15",
            14000,
            120.00,
            "Completed",
            "Engine oil and oil filter replaced."
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
            2,
            "Full Service",
            "2026-07-10",
            9500,
            350.00,
            "Completed",
            "Full vehicle inspection completed."
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
            3,
            "Brake Inspection",
            "2026-08-05",
            5000,
            80.00,
            "Completed",
            "Brake system inspected and checked."
        )
    )

    connection.commit()
    connection.close()

    total_service_records = get_total_service_records()

    assert total_service_records == 3


def test_get_vehicles_needing_service(monkeypatch, test_database):
    monkeypatch.setattr(
        "app.services.dashboard_service.get_connection",
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
            "C-Class",
            2024,
            "MB24 CCL",
            "WDD12345678901231",
            15000,
            "Petrol"
        )
    )

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
            "WDD12345678901232",
            25000,
            "Diesel"
        )
    )

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
            2025,
            "MB25 SCL",
            "WDD12345678901235",
            10000,
            "Petrol"
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
            1,
            "Full Service",
            "2026-06-15",
            10000,
            350.00,
            "Completed",
            "Full vehicle service completed."
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
            2,
            "Oil Change",
            "2026-07-10",
            20000,
            120.00,
            "Completed",
            "Engine oil and oil filter replaced."
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
            3,
            "Full Service",
            "2026-08-05",
            5000,
            350.00,
            "Completed",
            "Full vehicle inspection completed."
        )
    )

    connection.commit()
    connection.close()

    vehicles_needing_service = get_vehicles_needing_service()

    assert vehicles_needing_service == 2


def test_get_dashboard_summary(monkeypatch):
    monkeypatch.setattr(
        "app.services.dashboard_service.get_total_vehicles",
        lambda: 3
    )

    monkeypatch.setattr(
        "app.services.dashboard_service.get_total_service_records",
        lambda: 3
    )

    monkeypatch.setattr(
        "app.services.dashboard_service.get_vehicles_needing_service",
        lambda: 2
    )

    summary = get_dashboard_summary()
    assert summary == {
        "total_vehicles": 3,
        "total_service_records": 3,
        "vehicles_needing_service": 2
    }
