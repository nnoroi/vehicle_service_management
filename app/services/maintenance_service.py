from app.database.connection import get_connection
from app.models.service_record import ServiceRecord
from app.services.service_record_mapper import row_to_service_record


def get_last_service_for_vehicle(vehicle_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM service_records
        WHERE vehicle_id = ?
        ORDER BY service_date DESC, id DESC
        LIMIT 1
        """,
        (vehicle_id,)
    ).fetchone()

    connection.close()
    if not row:
        return None
    return row_to_service_record(row)


def get_previous_service_for_vehicle(vehicle_id, record_id, service_date):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM service_records
        WHERE vehicle_id = ?
          AND id != ?
          AND service_date <= ?
        ORDER BY service_date DESC, id DESC
        LIMIT 1
        """,
        (vehicle_id, record_id, service_date)
    ).fetchone()

    connection.close()

    if not row:
        return None

    return row_to_service_record(row)


def get_next_service_for_vehicle(vehicle_id, record_id, service_date):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM service_records
        WHERE vehicle_id = ?
            AND id != ?
            AND service_date >= ?
        ORDER BY service_date ASC, id ASC
        LIMIT 1
        """,
        (vehicle_id, record_id, service_date)
    ).fetchone()

    connection.close()

    if not row:
        return None

    return row_to_service_record(row)


def get_next_service_mileage(vehicle_id):
    last_service = get_last_service_for_vehicle(vehicle_id)

    if last_service is None:
        return None

    return last_service.mileage + 10000


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
