from app.models.vehicle import Vehicle
from app.services.vehicle_service import (
    get_vehicle_by_id,
    delete_vehicle
)


vehicle_id = 4

vehicle = get_vehicle_by_id(vehicle_id)

if vehicle:
    print(f"Found: {vehicle.make} {vehicle.model}")
else:
    print(f"No vehicle found with ID {vehicle_id}")

deleted = delete_vehicle(vehicle_id)

print(f"Deleted: {deleted}")

vehicle = get_vehicle_by_id(vehicle_id)

if vehicle is None:
    print("Successfully deleted")
else:
    print(f"Vehicle still exists: {vehicle.make} {vehicle.model}")
