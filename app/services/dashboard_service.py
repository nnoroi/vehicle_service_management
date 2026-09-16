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



def get_dashboard_summary():
    total_vehicles = get_total_vehicles()
    total_service_records = get_total_service_records()
    total_vehicles_needing_service = get_vehicles_needing_service()

    return {
        "total_vehicles": total_vehicles,
        "total_service_records": total_service_records,
        "vehicles_needing_service": total_vehicles_needing_service
    }



def get_vehicles_needing_service_list():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            vehicles.id,
            vehicles.make,
            vehicles.model,
            vehicles.year,
            vehicles.mileage,
            COUNT(service_records.id) AS service_record_count
        FROM vehicles
        LEFT JOIN service_records
            ON vehicles.id = service_records.vehicle_id
        GROUP BY
            vehicles.id,
            vehicles.make,
            vehicles.model,
            vehicles.year,
            vehicles.mileage
        """
    ).fetchall()

    connection.close()

    vehicles = []

    for car in rows:
        if is_service_due(car["id"], car["mileage"]):
            vehicles.append(car)

    return vehicles


def get_vehicle_service_record_count(vehicle_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT COUNT(*) AS total
        FROM service_records
        WHERE vehicle_id = ?
        """,
        (vehicle_id,)
    ).fetchone()

    connection.close()

    return row["total"]

def get_recent_service_records(limit=5):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT 
            service_records.id,
            service_records.vehicle_id,
            service_records.service_type,
            service_records.service_date,
            service_records.mileage,
            service_records.cost,
            service_records.status,
            vehicles.make,
            vehicles.model
        FROM service_records
        JOIN vehicles 
            ON service_records.vehicle_id = vehicles.id
        ORDER BY service_records.service_date DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    connection.close()
    return rows