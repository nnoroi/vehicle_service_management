from app import create_app


def test_get_vehicles(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "MB25 ABC",
            "WDD12345678901234",
            5000,
            "Petrol"
        )

    )

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.get("/vehicles")

    assert response.status_code == 200
    assert b"Vehicles" in response.data
    assert b"Mercedes-Benz" in response.data   
    assert b"E-Class" in response.data
    assert b"MB25 ABC" in response.data


def test_get_vehicle(test_database, monkeypatch):
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
            "MB25 ABC",
            "WDD12345678901234",
            5000,
            "Petrol"
        )

    )
    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.get(f"/vehicles/{vehicle_id}")

        
    assert response.status_code == 200
    assert b"Mercedes-Benz" in response.data
    assert b"E-Class" in response.data
    assert b"MB25 ABC" in response.data
    assert b"WDD12345678901234" in response.data
    assert b"5000" in response.data
    assert b"Petrol" in response.data


def test_get_vehicle_not_found(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.get("/vehicles/9999")

    assert response.status_code == 404
    assert b"Vehicle not found" in response.data


def test_create_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()
    with app.test_client() as client:
        response = client.post(
            "/vehicles",
            json={
                "make": "Mercedes-Benz",
                "model": "C-Class",
                "year": 2024,
                "registration": "MB24 CLC",
                "vin": "W1K12345678901234",
                "mileage": 15000,
                "fuel_type": "Petrol"
            }
        )
    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 1
    assert data["make"] == "Mercedes-Benz"
    assert data["model"] == "C-Class"
    assert data["year"] == 2024


def test_create_empty_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()
    with app.test_client() as client:
        response = client.post("/vehicles", json={})
    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Request body must contain JSON data"


def test_create_vehicle_missing_fields(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )
    app = create_app()
    with app.test_client() as client:
        response = client.post("/vehicles",
                               json={
                                   "make": "Mercedes-Benz",
                                   "model": "E-Class"
                               })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Missing required fields"
    assert data["fields"] == ["year", "registration", "mileage", "fuel_type"]


def test_create_invalid_mileage_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()
    with app.test_client() as client:
        response = client.post("/vehicles",
                               json={
                                   "make": "Mercedes-Benz",
                                   "model": "C-Class",
                                   "year": 2024,
                                   "registration": "MB24 CLC",
                                   "vin": "W1K12345678901234",
                                   "mileage": -500,
                                   "fuel_type": "Petrol"
                               })
    assert response.status_code == 400

    data = response.get_json()
    assert "Mileage cannot be negative" in data["error"]


def test_create_invalid_year_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()
    with app.test_client() as client:
        response = client.post("/vehicles",
                               json={
                                   "make": "Mercedes-Benz",
                                   "model": "C-Class",
                                   "year": 1800,
                                   "registration": "MB24 CLC",
                                   "vin": "W1K12345678901234",
                                   "mileage": 11500,
                                   "fuel_type": "Petrol"
                               })
    assert response.status_code == 400

    data = response.get_json()
    assert "Year must be a 1886 or later" in data["error"]


def test_empty_data(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()
    with app.test_client() as client:
        response = client.post("/vehicles")
    assert response.status_code == 400

    data = response.get_json(silent=True)
    assert data["error"] == "Request body must contain JSON data"


def test_update_vehicle(test_database, monkeypatch):
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
        response = client.put(f"/vehicles/{vehicle_id}",
                              json={
                                  "model": "C-Class AMG",
                                  "mileage": 20000
        }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == vehicle_id
    assert data["make"] == "Mercedes-Benz"
    assert data["model"] == "C-Class AMG"
    assert data["mileage"] == 20000
    assert data["year"] == 2024
    assert data["fuel_type"] == "Petrol"


def test_update_vehicle_not_found(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()
    with app.test_client() as client:
        response = client.put("/vehicles/9999",
                              json={
                                  "mileage": 20000
                              }
                              )
    assert response.status_code == 404

    data = response.get_json()
    assert data["error"] == "Vehicle not found"


def test_update_vehicle_invalid_mileage(test_database, monkeypatch):
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
            10000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.put(f"/vehicles/{vehicle_id}",
                              json={
                                  "mileage": -500
        })

    assert response.status_code == 400

    data = response.get_json()

    assert "Mileage cannot be negative" in data["error"]


def test_delete_vehicle(test_database, monkeypatch):
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
            "S-Class",
            2025,
            "MB25 SCL",
            "WDD12345678901235",
            5000,
            "Petrol"
        )
    )

    vehicle_id = cursor.lastrowid

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.delete(f"/vehicles/{vehicle_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Vehicle deleted successfully."

    connection = test_database()

    row = connection.execute(
        "SELECT * FROM vehicles WHERE id = ?",
        (vehicle_id,)).fetchone()

    connection.close()

    assert row is None


def test_delete_vehicle_not_found(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.delete("/vehicles/9999")

    assert response.status_code == 404

    data = response.get_json()
    assert data["error"] == "Vehicle not found."


def test_get_vehicle_maintenance(monkeypatch, test_database):
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
            "TEST111",
            "WDDTEST111234567",
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
            52000,
            250,
            "Completed",
            "Full service completed"
        )
    )

    test_connection.commit()
    test_connection.close()

    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.get(f"/vehicles/{vehicle_id}/maintenance")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "Service Not Due"
    assert data["next_service_mileage"] == 62000
    assert data["miles_remaining"] == 12000


def test_get_non_existed_vehicle_maintenance(monkeypatch, test_database):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    monkeypatch.setattr(
        "app.services.maintenance_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.get("/vehicles/9999/maintenance")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Vehicle not found."





def test_add_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
        test_database
    )

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/vehicles/add",
            data={
                "make": "Mercedes-Benz",
                "model": "C-Class",
                "year": "2025",
                "registration": "MB25 CCL",
                "vin": "WDD12345678901233",
                "mileage": "10000",
                "fuel_type": "Petrol"
            }
        )

    assert response.status_code == 302
    assert response.location.endswith("/vehicles/1")


def test_edit_vehicle(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            "MB25 EDT",
            "WDD12345678901235",
            30000,
            "Diesel"
        )
    )

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/vehicles/1/edit",
            data={
                "make": "Mercedes-Benz",
                "model": "E-Class",
                "year": "2025",
                "registration": "MB25 EDT",
                "vin": "WDD12345678901235",
                "mileage": "45000",
                "fuel_type": "Diesel"
            }
        )

    assert response.status_code == 302
    assert response.location.endswith("/vehicles/1")

    connection = test_database()

    row = connection.execute(
        "SELECT mileage FROM vehicles WHERE id = ?",
        (1,)
    ).fetchone()
    connection.close()
    assert row["mileage"] == 45000


def test_delete_vehicle_page(test_database, monkeypatch):
    monkeypatch.setattr(
        "app.services.vehicle_service.get_connection",
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
            2025,
            "MB25 DEL",
            "WDD12345678901236",
            30000,
            "Petrol"
        )
    )

    connection.commit()
    connection.close()

    app = create_app()

    with app.test_client() as client:
        response = client.post("/vehicles/1/delete")

    assert response.status_code == 302
    assert response.location.endswith("/vehicles")

    connection = test_database()

    row = connection.execute(
        "SELECT * FROM vehicles WHERE id = ?",
        (1,)
    ).fetchone()

    connection.close()

    assert row is None