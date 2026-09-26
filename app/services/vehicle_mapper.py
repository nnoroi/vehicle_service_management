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
