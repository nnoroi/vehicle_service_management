from app.services.maintenance_service import (
    get_last_service_for_vehicle,
    get_next_service_mileage,
    is_service_due,
    get_miles_until_service,
    get_maintenance_status
)


def test_get_last_service_for_vehicle(monkeypatch, test_database):
    test_connection = test_database()

    cursor = test_connection.execute(
        """
        INSERT INTO vehicles
        (make, model, year, registration, vin, mileage, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "E-Class",
            2024,
            "TEST123",
            "WDDTEST123456789",
            30000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Oil Change",
            "2026-08-01",
            30000,
            85,
            "Completed",
            "Oil changed"
        )
    )

    test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-09-10",
            32000,
            250,
            "Completed",
            "Full service completed"
        )
    )

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    record = get_last_service_for_vehicle(vehicle_id)

    assert record is not None
    assert record.vehicle_id == vehicle_id
    assert record.service_type == "Full Service"
    assert record.service_date == "2026-09-10"
    assert record.mileage == 32000
    assert record.cost == 250
    assert record.status == "Completed"
    assert record.notes == "Full service completed"


def test_get_last_service_for_vehicle_not_found(monkeypatch, test_database):
    test_connection = test_database()

    cursor = test_connection.execute(
        """
        INSERT INTO vehicles
        (make, model, year, registration, vin, mileage, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "C-Class",
            2023,
            "TEST456",
            "WDDTEST456789012",
            20000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    record = get_last_service_for_vehicle(vehicle_id)

    assert record is None


def test_get_next_service_mileage(monkeypatch, test_database):
    test_connection = test_database()

    cursor = test_connection.execute(
        """
        INSERT INTO vehicles
        (make, model, year, registration, vin, mileage, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "C-Class",
            2023,
            "TEST789",
            "WDDTEST789012345",
            50000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-09-10",
            50000,
            250,
            "Completed",
            "Full service completed"
        )
    )

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    next_mileage = get_next_service_mileage(vehicle_id)

    assert next_mileage == 60000


def test_is_service_due(monkeypatch, test_database):
    test_connection = test_database()

    cursor = test_connection.execute(
        """
        INSERT INTO vehicles
        (make, model, year, registration, vin, mileage, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "E-Class",
            2024,
            "TEST999",
            "WDDTEST999012345",
            50000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-09-10",
            50000,
            250,
            "Completed",
            "Full service completed"
        )
    )

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    assert is_service_due(vehicle_id, 60000) is True
    assert is_service_due(vehicle_id, 55000) is False


def test_get_miles_until_service(monkeypatch, test_database):
    test_connection = test_database()

    cursor = test_connection.execute(
        """
        INSERT INTO vehicles
        (make, model, year, registration, vin, mileage, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "S-Class",
            2024,
            "TEST321",
            "WDDTEST321012345",
            50000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-09-10",
            50000,
            300,
            "Completed",
            "Full service completed"
        )
    )

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    assert get_miles_until_service(vehicle_id, 54000) == 6000
    assert get_miles_until_service(vehicle_id, 60000) == 0
    assert get_miles_until_service(vehicle_id, 65000) == 0


def test_get_maintenance_status(monkeypatch, test_database):
    test_connection = test_database()

    cursor = test_connection.execute(
        """
        INSERT INTO vehicles
        (make, model, year, registration, vin, mileage, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "E-Class",
            2024,
            "TEST654",
            "WDDTEST654012345",
            54000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-09-10",
            50000,
            250,
            "Completed",
            "Full service completed"
        )
    )

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    status = get_maintenance_status(vehicle_id, 54000)

    assert status["status"] == "Service Not Due"
    assert status["next_service_mileage"] == 60000
    assert status["miles_remaining"] == 6000


def test_get_maintenance_status_service_due(monkeypatch, test_database):
    test_connection = test_database()

    cursor = test_connection.execute(
        """
        INSERT INTO vehicles
        (make, model, year, registration, vin, mileage, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Mercedes-Benz",
            "C-Class",
            2023,
            "TEST987",
            "WDDTEST987012345",
            65000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Full Service",
            "2026-09-10",
            50000,
            250,
            "Completed",
            "Full service completed"
        )
    )

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    status = get_maintenance_status(vehicle_id, 65000)

    assert status["status"] == "Service Due"
    assert status["next_service_mileage"] == 60000
    assert status["miles_remaining"] == 0
