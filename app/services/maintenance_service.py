from app.database.connection import get_connection
from app.models.service_record import ServiceRecord


def get_last_service_for_vehicle(vehicle_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM service_records
        WHERE vehicle_id = ?
        ORDER BY service_date DESC
        LIMIT 1
        """,
        (vehicle_id,)
    ).fetchone()

    connection.close()
    if not row:
        return None
    return ServiceRecord(
        vehicle_id=row["vehicle_id"],
        service_type=row["service_type"],
        service_date=row["service_date"],
        mileage=row["mileage"],
        cost=row["cost"],
        status=row["status"],
        notes=row["notes"],
        record_id=row["id"]
    )


def get_next_service_mileage(vehicle_id):
    connection = get_connection()
    row = connection.execute(
        """
        SELECT mileage
        FROM service_records
        WHERE vehicle_id = ?
        ORDER BY mileage DESC
        LIMIT 1
        """,
        (vehicle_id,)
    ).fetchone()

    connection.close()

    if not row:
        return None
    return row["mileage"] + 10000


def is_service_due(vehicle_id, current_mileage):
    next_service_mileage = get_next_service_mileage(vehicle_id)

    if next_service_mileage is None:
        return True
    return current_mileage >= next_service_mileage


def get_miles_until_service(vehicle_id, current_mileage):
    next_service_mileage = get_next_service_mileage(vehicle_id)

    if next_service_mileage is None:
        return 0
    miles_remaining = next_service_mileage - current_mileage
    return max(miles_remaining, 0)


def get_maintenance_status(vehicle_id, current_mileage):
    next_service_mileage = get_next_service_mileage(vehicle_id)
    if next_service_mileage is None:
        return {
            "status": "Service Due",
            "next_service_mileage": None,
            "miles_remaining": 0
        }

    miles_remaining = max(next_service_mileage - current_mileage, 0)

    if current_mileage >= next_service_mileage:
        status = "Service Due"
    else:
        status = "Service Not Due"

    return {
        "status": status,
        "next_service_mileage": next_service_mileage,
        "miles_remaining": miles_remaining
    }
