from app.database.connection import get_connection
from app.models.vehicle import Vehicle
from app.validators.vehicle_validator import validate_vehicle


def create_vehicle(vehicle):
    """Add a new vehicle to the database."""

    errors = validate_vehicle(vehicle)

    if errors:
        raise ValueError("\n".join(errors))

    connection = get_connection()
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
            vehicle.make,
            vehicle.model,
            vehicle.year,
            vehicle.registration,
            vehicle.vin,
            vehicle.mileage,
            vehicle.fuel_type
        )
    )
    connection.commit()
    vehicle.id = cursor.lastrowid
    connection.close()
    return vehicle


def get_vehicle_by_id(vehicle_id):
    """Get a vehicle from the database by its ID"""
    connection = get_connection()
    cursor = connection.execute(
        "SELECT * FROM vehicles WHERE id = ?", (vehicle_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return Vehicle(
        vehicle_id=row["id"],
        make=row["make"],
        model=row["model"],
        year=row["year"],
        registration=row["registration"],
        vin=row["vin"],
        mileage=row["mileage"],
        fuel_type=row["fuel_type"]
    )


def get_all_vehicles():
    """Get all vehicles from the database"""
    connection = get_connection()
    cursor = connection.execute("SELECT * FROM vehicles ORDER BY id")
    rows = cursor.fetchall()
    connection.close()
    vehicles = []

    for row in rows:
        vehicle = Vehicle(
            vehicle_id=row["id"],
            make=row["make"],
            model=row["model"],
            year=row["year"],
            registration=row["registration"],
            vin=row["vin"],
            mileage=row["mileage"],
            fuel_type=row["fuel_type"]
        )
        vehicles.append(vehicle)

    return vehicles


def update_vehicle(vehicle):
    """Update an existing vehicle in the database"""

    errors = validate_vehicle(vehicle)
    if errors:
        raise ValueError("\n".join(errors))

    connection = get_connection()
    cursor = connection.execute(
        """
        UPDATE vehicles
        SET 
            make = ?,
            model = ?,
            year = ?,
            registration = ?,
            vin = ?,
            mileage = ?,
            fuel_type = ?
        WHERE id = ? 
        """,
        (
            vehicle.make,
            vehicle.model,
            vehicle.year,
            vehicle.registration,
            vehicle.vin,
            vehicle.mileage,
            vehicle.fuel_type,
            vehicle.id
        )
    )
    connection.commit()
    connection.close()
    return cursor.rowcount > 0  # Return True if a row was updated, False otherwise


def delete_vehicle(vehicle_id):
    """Delete a vehicle from the database"""
    connection = get_connection()
    cursor = connection.execute(
        "DELETE FROM vehicles WHERE id =?", (vehicle_id,)
    )

    connection.commit()
    connection.close()
    return cursor.rowcount > 0  # Return True if a row was deleted, False otherwise
