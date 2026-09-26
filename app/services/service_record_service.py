from app.database.connection import get_connection
from app.models.service_record import ServiceRecord
from app.validators.service_record_validator import validate_service_record
from app.services.vehicle_service import get_vehicle_by_id
from app.services.maintenance_service import (
    get_last_service_for_vehicle,
    get_previous_service_for_vehicle,
    get_next_service_for_vehicle
)
from app.services.service_record_mapper import row_to_service_record


def create_service_record(record):
    """Add a new service record to the database"""

    errors = validate_service_record(record)

    if errors:
        raise ValueError("\n".join(errors))

    vehicle = get_vehicle_by_id(record.vehicle_id)
    if vehicle is None:
        raise ValueError(
            f"Vehicle with ID {record.vehicle_id} does not exist."
        )

    last_service = get_last_service_for_vehicle(record.vehicle_id)

    if last_service and record.mileage < last_service.mileage:
        raise ValueError(
            f"Service mileage cannot be lower than the previous "
            f"service mileage of {last_service.mileage} miles."
        )

    connection = get_connection()
    cursor = connection.execute(
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
            record.vehicle_id,
            record.service_type,
            record.service_date,
            record.mileage,
            record.cost,
            record.status,
            record.notes
        )
    )
    connection.commit()
    record.id = cursor.lastrowid
    connection.close()
    return record


def get_records_by_vehicle_id(vehicle_id):
    """Get all service records for a specific vehicle from the database"""

    connection = get_connection()
    cursor = connection.execute(
        """
        SELECT * 
        FROM service_records 
        WHERE vehicle_id = ? 
        ORDER BY service_date DESC, id DESC
        """,
        (vehicle_id,)
    )
    rows = cursor.fetchall()
    connection.close()
    return [row_to_service_record(row) for row in rows]


def get_service_history_summary(vehicle_id):
    """Get summary information about a vehicle's service history"""

    connection = get_connection()
    cursor = connection.execute(
        """
        SELECT 
            COUNT(*) AS total_services,
            MAX(service_date) AS last_service_date,
            (
                SELECT mileage 
                FROM service_records 
                WHERE vehicle_id =? 
                ORDER BY service_date DESC, id DESC
                LIMIT 1
            ) AS last_service_mileage,
            COALESCE(SUM(cost), 0) AS total_cost
        FROM service_records
        WHERE vehicle_id = ?
        """,
        (vehicle_id, vehicle_id)
    )

    row = cursor.fetchone()
    connection.close()

    return {
        "total_services": row["total_services"],
        "last_service_date": row["last_service_date"],
        "last_service_mileage": row["last_service_mileage"],
        "total_cost": row["total_cost"]
    }


def get_service_record_by_id(record_id):
    """Get a specific service record from the database"""

    connection = get_connection()
    cursor = connection.execute(
        "SELECT * FROM service_records WHERE id = ?",
        (record_id,)
    )
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None

    return row_to_service_record(row)


def update_service_record(record):
    """Update an existing service record in the database"""

    errors = validate_service_record(record)
    if errors:
        raise ValueError("\n".join(errors))

    existing_record = get_service_record_by_id(record.id)

    if existing_record is None:
        return False

    previous_service = get_previous_service_for_vehicle(
        record.vehicle_id,
        record.id,
        record.service_date)

    if previous_service and record.mileage < previous_service.mileage:
        raise ValueError(
            f"Service mileage cannot be lower than the previous "
            f"service mileage of {previous_service.mileage} miles."
        )

    next_service = get_next_service_for_vehicle(
        record.vehicle_id,
        record.id,
        record.service_date
    )

    if next_service and record.mileage > next_service.mileage:
        raise ValueError(
            f"Service mileage cannot be higher than the next "
            f"service mileage of {next_service.mileage} miles."
        )
    connection = get_connection()
    cursor = connection.execute(
        """
        UPDATE service_records
        SET
            vehicle_id = ?,
            service_type = ?,
            service_date = ?,
            mileage = ?,
            cost = ?,
            status = ?,
            notes = ?
        WHERE id = ?
        """,
        (
            record.vehicle_id,
            record.service_type,
            record.service_date,
            record.mileage,
            record.cost,
            record.status,
            record.notes,
            record.id
        )
    )
    connection.commit()
    connection.close()
    return cursor.rowcount > 0


def get_all_records():
    """"Get all service records from the database"""
    connection = get_connection()
    cursor = connection.execute(
        """SELECT * FROM service_records ORDER BY service_date DESC"""
    )

    rows = cursor.fetchall()
    connection.close()
    return [row_to_service_record(row) for row in rows]


def delete_service_record(record_id):
    """Delete a service record from the database"""

    connection = get_connection()
    cursor = connection.execute(
        """DELETE FROM service_records WHERE id = ?""", (record_id,)
    )
    connection.commit()
    connection.close()
    return cursor.rowcount > 0
