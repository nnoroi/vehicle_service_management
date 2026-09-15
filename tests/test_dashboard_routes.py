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

    app = create_app()
    with app.test_client() as client:
        response = client.get("/dashboard")

    data = response.get_json()

    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"3" in response.data
    assert b"2" in response.data
