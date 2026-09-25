from app import create_app


def test_get_vehicle_services(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "WDD12345678901234",
            50000,
            "Petrol"
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
            "Oil Change",
            "2026-08-29",
            50000,
            85,
            "Completed",
            "Oil and filter replaced"
        )
    )

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.get(f"/vehicles/{vehicle_id}/services")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["vehicle_id"] == vehicle_id
    assert data[0]["service_type"] == "Oil Change"
    assert data[0]["service_date"] == "2026-08-29"
    assert data[0]["mileage"] == 50000
    assert data[0]["cost"] == 85
    assert data[0]["status"] == "Completed"
    assert data[0]["notes"] == "Oil and filter replaced"


def test_get_vehicle_services_empty(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "C-Class",
            2024,
            "MB24 CLC",
            "W1K12345678901234",
            15000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.get(f"/vehicles/{vehicle_id}/services")

    assert response.status_code == 200

    data = response.get_json()

    assert data == []


def test_get_vehicle_services_not_found(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()
    with app.test_client() as client:
        response = client.get("/vehicles/9999/services")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Vehicle not found."


def test_create_vehicle_service(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "WDD12345678901234",
            50000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            f"/vehicles/{vehicle_id}/services",
            json={
                "service_type": "Oil Change",
                "service_date": "2026-09-10",
                "mileage": 52000,
                "cost": 85,
                "status": "Completed",
                "notes": "Oil and filter replaced"
            }
        )

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 1
    assert data["vehicle_id"] == vehicle_id
    assert data["service_type"] == "Oil Change"
    assert data["service_date"] == "2026-09-10"
    assert data["mileage"] == 52000
    assert data["cost"] == 85
    assert data["status"] == "Completed"
    assert data["notes"] == "Oil and filter replaced"


def test_create_vehicle_service_missing_fields(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "C-Class",
            2024,
            "MB24 CLC",
            "W1K12345678901234",
            15000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            f"/vehicles/{vehicle_id}/services",
            json={
                "service_type": "MOT"
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required fields"
    assert data["fields"] == [
        "service_date",
        "mileage",
        "cost",
        "status"
    ]


def test_create_vehicle_service_invalid_mileage(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "WDD12345678901234",
            50000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            f"/vehicles/{vehicle_id}/services",
            json={
                "service_type": "Oil Change",
                "service_date": "2026-09-10",
                "mileage": -500,
                "cost": 85,
                "status": "Completed",
                "notes": "Oil and filter replaced"
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert "Mileage cannot be negative" in data["error"]


def test_get_service(monkeypatch, test_database):
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

    cursor = test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Oil Change",
            "2026-09-10",
            30000,
            85,
            "Completed",
            "Oil changed"
        )
    )

    service_id = cursor.lastrowid

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )
    app = create_app()
    with app.test_client() as client:
        response = client.get(f"/services/{service_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == service_id
    assert data["vehicle_id"] == vehicle_id
    assert data["service_type"] == "Oil Change"
    assert data["service_date"] == "2026-09-10"
    assert data["mileage"] == 30000
    assert data["cost"] == 85
    assert data["status"] == "Completed"
    assert data["notes"] == "Oil changed"


def test_get_service_not_found(monkeypatch, test_database):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )
    app = create_app()
    with app.test_client() as client:
        response = client.get("/services/9999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Service record not found."


def test_update_service(monkeypatch, test_database):
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

    cursor = test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Oil Change",
            "2026-09-10",
            30000,
            85,
            "Completed",
            "Oil changed"
        )
    )

    service_id = cursor.lastrowid

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.put(
            f"/services/{service_id}",
            json={
                "cost": 120,
                "notes": "Oil and filter replaced"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == service_id
    assert data["vehicle_id"] == vehicle_id
    assert data["service_type"] == "Oil Change"
    assert data["service_date"] == "2026-09-10"
    assert data["mileage"] == 30000
    assert data["cost"] == 120
    assert data["status"] == "Completed"
    assert data["notes"] == "Oil and filter replaced"


def test_update_service_not_found(monkeypatch, test_database):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.put(
            "/services/9999",
            json={
                "cost": 120
            }
        )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Service record not found."


def test_update_service_missing_json():
    app = create_app()

    with app.test_client() as client:
        response = client.put("services/9999")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Request body must contain JSON data"


def test_create_vehicle_service_invalid_json():
    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/vehicles/9999/services",
            data='{"service_type": "Oil Change',
            content_type="application/json"
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Request body must contain JSON data"


def test_delete_service(monkeypatch, test_database):
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

    cursor = test_connection.execute(
        """
        INSERT INTO service_records
        (vehicle_id, service_type, service_date, mileage, cost, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_id,
            "Oil Change",
            "2026-09-10",
            30000,
            85,
            "Completed",
            "Oil changed"
        )
    )

    service_id = cursor.lastrowid

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.delete(f"/services/{service_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Service record deleted successfully."


def test_delete_service_not_found(monkeypatch, test_database):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.delete("/services/9999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Service record not found."


def test_get_service_not_found():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/services/9999")

        assert response.status_code == 404

        data = response.get_json()

        assert data["error"] == "Service record not found."


def test_service_details_not_found():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/services/9999/details")

    assert response.status_code == 404
    assert b"Service record not found" in response.data


def test_create_vehicle_service_missing_json():
    app = create_app()
    with app.test_client() as client:
        response = client.post("/vehicles/9999/services")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Request body must contain JSON data"


def test_create_vehicle_service_vehicle_not_found():
    app = create_app()
    with app.test_client() as client:
        response = client.post(
            "/vehicles/9999/services",
            json={
                "service_type": "Oil Change",
                "service_date": "2026-09-17",
                "mileage": 40000,
                "cost": 75.00,
                "status": "Completed"
            }
        )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Vehicle not found."


def test_create_vehicle_service_missing_fields(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.service_record_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "C-Class",
            2024,
            "MB24 CLC",
            "W1K12345678901234",
            15000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            f"/vehicles/{vehicle_id}/services",
            json={
                "service_type": "Oil Change",
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required fields"
    assert data["fields"] == [
        "service_date",
        "mileage",
        "cost",
        "status"
    ]


def test_create_vehicle_service_empty_json():

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            f"/vehicles/9999/services",
            json={}
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Request body must contain JSON data"
