from app.models.service_record import ServiceRecord


def row_to_service_record(row):
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
