from datetime import datetime


VALID_STATUSES = {
    "Scheduled",
    "In Progress",
    "Completed",
    "Cancelled"
}


def validate_service_record(record):
    """Validate service record data"""

    errors = []

    if not isinstance(record.vehicle_id, int) or record.vehicle_id <= 0:
        errors.append("Vehicle ID must be a positive number.")

    if not isinstance(record.service_type, str) or not record.service_type.strip():
        errors.append("Service type is required.")

    if not record.service_date:
        errors.append("Service date is required.")

    else:
        try:
            datetime.strptime(record.service_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Service date must be a valid date.")

    if not isinstance(record.mileage, (int, float)):
        errors.append("Mileage must be a number.")
    elif record.mileage < 0:
        errors.append("Mileage cannot be negative.")

    if not isinstance(record.cost, (int, float)):
        errors.append("Cost must be a number.")
    elif record.cost < 0:
        errors.append("Cost cannot be negative.")

    if record.status not in VALID_STATUSES:
        errors.append(
            "Status must be Scheduled, In Progress, "
            "Completed, or Cancelled."
        )

    return errors
