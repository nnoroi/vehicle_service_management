from app.models.service_record import ServiceRecord
from app.services.service_record_service import create_service_record, get_records_by_vehicle_id, get_service_record_by_id, update_service_record, delete_service_record

record = ServiceRecord(
    vehicle_id=1,
    service_type="Oil Change",
    service_date="2023-10-01",
    mileage=50000,
    cost=50.00,
    status="Completed",
    notes="Regular oil change performed"
)

created_record = create_service_record(record)
print(f"Service record created with ID: {created_record.id}")


vehicle_id = created_record.vehicle_id
records = get_records_by_vehicle_id(vehicle_id)

print(f"Service records for vehicle ID {vehicle_id}:")
for record in records:
    print(
        f"ID: {record.id}"
        f", Type: {record.service_type}"
        f", Cost: {record.cost}")


record.cost = 75.00
record.notes = "Oil and filter change performed"

updated = update_service_record(record)
print(f"Service record updated: {updated}")

updated_record = get_service_record_by_id(record.id)

print(f"Updated cost: {updated_record.cost}")
print(f"Updated notes: {updated_record.notes}")

deleted = delete_service_record(record.id)
print(f"Deleted record: {deleted}")

deleted_record = get_service_record_by_id(record.id)
print(f"Record after deletion: {deleted_record}")
