from app.database.connection import get_connection
from app.services.maintenance_service import is_service_due


def get_total_vehicles():
    connection = get_connection()

    row = connection.execute(
        # counts total rows and assigns to total
        "SELECT COUNT(*) AS total FROM vehicles"
    ).fetchone()
    connection.close()
    return row["total"]


def get_total_service_records():
    connection = get_connection()
    row = connection.execute(
        "SELECT COUNT(*) AS total FROM service_records"
    ).fetchone()
    connection.close()
    return row["total"]


def get_vehicles_needing_service():
    connection = get_connection()
    row = connection.execute(
        "SELECT id, mileage FROM vehicles"
    ).fetchall()
    connection.close()
    total = 0
    for car in row:
        if is_service_due(car["id"], car["mileage"]):
            total += 1

    return total

def get_vehicles_needing_service_list():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, make, model, year, mileage FROM vehicles"
    ).fetchall()

    connection.close()

    vehicles = []

    for car in rows:
        if is_service_due(car["id"], car["mileage"]):
            vehicles.append(car)

    return vehicles


def get_dashboard_summary():
    total_vehicles = get_total_vehicles()
    total_service_records = get_total_service_records()
    total_vehicles_needing_service = get_vehicles_needing_service()

    return {
        "total_vehicles": total_vehicles,
        "total_service_records": total_service_records,
        "vehicles_needing_service": total_vehicles_needing_service
    }
