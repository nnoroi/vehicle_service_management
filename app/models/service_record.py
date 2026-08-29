class ServiceRecord:
    def __init__(
            self,
            vehicle_id,
            service_type,
            service_date,
            mileage,
            cost,
            status,
            notes=None,
            record_id=None
    ):
        self.id = record_id
        self.vehicle_id = vehicle_id
        self.service_type = service_type
        self.service_date = service_date
        self.mileage = mileage
        self.cost = cost
        self.status = status
        self.notes = notes
