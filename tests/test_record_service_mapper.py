from app.models.service_record import ServiceRecord
from app.services.service_record_mapper import service_record_to_dict


def test_service_record_to_dict():
    record = ServiceRecord(
        vehicle_id=1,
        service_type="Full Service",
        service_date="2026-09-15",
        mileage=40000,
        cost=250,
        status="Completed",
        notes="Full service completed",
        record_id=1
    )

    result = service_record_to_dict(record)

    assert result == {
        "id": 1,
        "vehicle_id": 1,
        "service_type": "Full Service",
        "service_date": "2026-09-15",
        "mileage": 40000,
        "cost": 250,
        "status": "Completed",
        "notes": "Full service completed"
    }
