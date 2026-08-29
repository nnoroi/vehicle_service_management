def validate_vehicle(vehicle):
    """Validate vehicle data before saving it to the database"""

    errors = []

    if not vehicle.make.strip():
        errors.append("Make is required.")
    if not vehicle.model.strip():
        errors.append("Model is required.")
    if not isinstance(vehicle.year, int):
        errors.append("Year must be a number.")
    elif vehicle.year < 1886:
        errors.append("Year must be a 1886 or later.")
    if not vehicle.registration.strip():
        errors.append("Registration is required.")
    if vehicle.mileage < 0:
        errors.append("Mileage cannot be negative.")
    if not vehicle.fuel_type.strip():
        errors.append("Fuel type is required.")

    return errors
