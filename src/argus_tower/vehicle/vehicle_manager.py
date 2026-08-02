from argus_tower.vehicle.vehicle import Vehicle

class VehicleManager:
    def __init__(self, max_vehicles: int = 8):
        self.vehicles = {}
        for i in range(1, max_vehicles + 1):
            self.vehicles[i] = Vehicle(vehicle_id=i)

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        return self.vehicles.get(vehicle_id)

    def get_all_vehicles(self):
        return list(self.vehicles.values())