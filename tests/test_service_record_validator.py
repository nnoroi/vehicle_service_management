from app.models.service_record import ServiceRecord
from app.validators.service_record_validator import validate_service_record


def test_valid_service_record():
    record = ServiceRecord(
        record_id=None,
        vehicle_id=2,
        service_type="Oil Change",
        service_date="31/08/2026",
        mileage=18500,
        cost=75.00,
        status="Completed",
        notes="Oil and filter replaced"
    )

    errors = validate_service_record(record)

    assert errors == []


def test_invalid_service_record():
    record = ServiceRecord(
        record_id=None,
        vehicle_id=-1,
        service_type="",
        service_date="",
        mileage=-500,
        cost=-10,
        status="Water",
        notes=""
    )

    errors = validate_service_record(record)

    assert "Vehicle ID must be a positive number." in errors
    assert "Service type is required." in errors
    assert "Service date is required." in errors
    assert "Mileage cannot be negative." in errors
    assert "Cost cannot be negative." in errors
    assert "Status must be Scheduled, In Progress, Completed, or Cancelled." in errors
