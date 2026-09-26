from app.models.vehicle import Vehicle


def row_to_vehicle(row):
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


def vehicle_to_dict(vehicle):
    return {
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "registration": vehicle.registration,
        "vin": vehicle.vin,
        "mileage": vehicle.mileage,
        "fuel_type": vehicle.fuel_type
    }
