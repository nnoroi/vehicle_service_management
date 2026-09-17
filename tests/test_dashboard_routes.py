from app import create_app


def test_dashboard_route(monkeypatch):
    monkeypatch.setattr(
        "app.routes.dashboard_routes.get_dashboard_summary",
        lambda: {
            "total_vehicles": 3,
            "total_service_records": 3,
            "vehicles_needing_service": 2
        }
    )

    monkeypatch.setattr(
        "app.routes.dashboard_routes.get_vehicles_needing_service_list",
        lambda: []
    )

    monkeypatch.setattr(
        "app.routes.dashboard_routes.get_recent_service_records",
        lambda: [
            {
                "id": 1,
                "vehicle_id": 1,
                "service_type": "Oil Change",
                "service_date": "2026-09-16",
                "mileage": 40000,
                "cost": 75.00,
                "status": "Completed",
                "make": "Mercedes-Benz",
                "model": "E-Class"
            }
        ]
    )

    app = create_app()

    with app.test_client() as client:
        response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"3" in response.data
    assert b"2" in response.data
    assert b"Oil Change" in response.data
    assert b"Mercedes-Benz" in response.data
    assert b"E-Class" in response.data
    assert b"Completed" in response.data
