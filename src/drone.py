import numpy as np

class Drone:
    def __init__(self, drone_id: int, position: tuple, fuel: float = 100.0, particle_capacity: float = 3000.0):
        self.drone_id = drone_id
        self.position = np.array(position, dtype=float)
        self.fuel = fuel
        self.max_fuel = 100.0
        self.particle_capacity = particle_capacity
        self.dispensed_kg = 0.0
        self.status = "NOMINAL"

    def update_state(self, elapsed_hours: float, consumption_multiplier: float = 1.0):
        safe_multiplier = min(consumption_multiplier, 2.0)
        fuel_burn_rate = 4.0 * safe_multiplier

        self.fuel = max(0.0, self.max_fuel - (elapsed_hours * fuel_burn_rate))

        operating_hours = min(elapsed_hours, self.max_fuel / fuel_burn_rate) if fuel_burn_rate > 0 else elapsed_hours
        dispense_rate = 120.0
        self.dispensed_kg = min(self.particle_capacity, operating_hours * dispense_rate)

        if self.fuel <= 0:
            self.status = "DEPLETED"
            self.fuel = 0.0
        elif self.fuel < 20.0:
            self.status = "LOW_FUEL"
        else:
            self.status = "NOMINAL"

    def update_telemetry(self, elapsed_hours: float, wind_vector=(0.0, 0.0)):
        self.update_state(elapsed_hours)

    def refuel(self):
        self.fuel = 100.0
        self.max_fuel = 100.0
        self.dispensed_kg = 0.0
        self.status = "NOMINAL"

    def get_dict(self):
        return {
            "drone_id": self.drone_id,
            "x": round(float(self.position[0]), 2),
            "y": round(float(self.position[1]), 2),
            "fuel_pct": round(float(self.fuel), 1),
            "dispensed_kg": round(float(self.dispensed_kg), 1),
            "status": self.status
        }