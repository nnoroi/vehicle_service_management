from app.database.connection import get_connection
from app.models.service_record import ServiceRecord
from app.validators.service_record_validator import validate_service_record
from app.services.vehicle_service import get_vehicle_by_id


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
        """SELECT * FROM service_records WHERE vehicle_id = ? ORDER BY service_date DESC""", (
            vehicle_id,)
    )
    rows = cursor.fetchall()
    connection.close()
    records = []
    for row in rows:
        record = ServiceRecord(
            record_id=row["id"],
            vehicle_id=row["vehicle_id"],
            service_type=row["service_type"],
            service_date=row["service_date"],
            mileage=row["mileage"],
            cost=row["cost"],
            status=row["status"],
            notes=row["notes"]
        )
        records.append(record)
    return records


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

    return ServiceRecord(
        record_id=row["id"],
        vehicle_id=row["vehicle_id"],
        service_type=row["service_type"],
        service_date=row["service_date"],
        mileage=row["mileage"],
        cost=row["cost"],
        status=row["status"],
        notes=row["notes"]
    )


def update_service_record(record):
    """Update an existing service record in the database"""

    errors = validate_service_record(record)
    if errors:
        raise ValueError("\n".join(errors))

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
    records = []
    for row in rows:
        record = ServiceRecord(
            record_id=row["id"],
            vehicle_id=row["vehicle_id"],
            service_type=row["service_type"],
            service_date=row["service_date"],
            mileage=row["mileage"],
            cost=row["cost"],
            status=row["status"],
            notes=row["notes"]
        )
        records.append(record)
    return records


def delete_service_record(record_id):
    """Delete a service record from the database"""

    connection = get_connection()
    cursor = connection.execute(
        """DELETE FROM service_records WHERE id = ?""", (record_id,)
    )
    connection.commit()
    connection.close()
    return cursor.rowcount > 0
