class Vehicle:
    def __init__(
            self,
            make,
            model,
            year,
            registration,
            vin,
            mileage,
            fuel_type,
            vehicle_id=None
    ):
        self.id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.registration = registration
        self.vin = vin
        self.mileage = mileage
        self.fuel_type = fuel_type
