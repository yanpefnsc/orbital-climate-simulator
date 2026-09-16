import numpy as np

REGIONAL_PROFILES = {
    "usa": {"base_irradiance": 1050.0, "wind_speed": 1.0, "aerosol_half_life_hours": 14.0},
    "eua": {"base_irradiance": 1050.0, "wind_speed": 1.0, "aerosol_half_life_hours": 14.0},
    "estados unidos": {"base_irradiance": 1050.0, "wind_speed": 1.0, "aerosol_half_life_hours": 14.0},
    "canada": {"base_irradiance": 950.0, "wind_speed": 1.2, "aerosol_half_life_hours": 10.0},
    "brazil": {"base_irradiance": 1020.0, "wind_speed": 1.1, "aerosol_half_life_hours": 7.0},
    "brasil": {"base_irradiance": 1020.0, "wind_speed": 1.1, "aerosol_half_life_hours": 7.0},
    "sao paulo": {"base_irradiance": 1020.0, "wind_speed": 1.1, "aerosol_half_life_hours": 7.0},
    "sp": {"base_irradiance": 1020.0, "wind_speed": 1.1, "aerosol_half_life_hours": 7.0},
    "mexico": {"base_irradiance": 1080.0, "wind_speed": 1.0, "aerosol_half_life_hours": 12.0},
    "argentina": {"base_irradiance": 950.0, "wind_speed": 1.3, "aerosol_half_life_hours": 11.0},
    "chile": {"base_irradiance": 1100.0, "wind_speed": 1.4, "aerosol_half_life_hours": 15.0},
    "atacama": {"base_irradiance": 1280.0, "wind_speed": 1.6, "aerosol_half_life_hours": 18.0},
    "colombia": {"base_irradiance": 980.0, "wind_speed": 0.9, "aerosol_half_life_hours": 6.0},
    "peru": {"base_irradiance": 1150.0, "wind_speed": 1.2, "aerosol_half_life_hours": 16.0},
    "default": {"base_irradiance": 1000.0, "wind_speed": 1.0, "aerosol_half_life_hours": 10.0}
}

class ClimateSimulator:
    def __init__(self, target_region: str, area_sq_km: float, desired_reduction_pct: float):
        self.target_region = target_region
        self.area_sq_km = area_sq_km
        self.desired_reduction_pct = desired_reduction_pct
        self.drones = []

        region_key = target_region.strip().lower()
        self.profile = REGIONAL_PROFILES.get(region_key, REGIONAL_PROFILES["default"])

    def add_drone(self, drone):
        self.drones.append(drone)

    def refuel_fleet(self):
        for drone in self.drones:
            drone.refuel()

    def run_simulation(self, current_hour: float):
        if not self.drones:
            return {}

        total_drones = len(self.drones)

        area_density_factor = np.sqrt(self.area_sq_km) / 100.0
        effective_hours = current_hour * self.profile["wind_speed"]

        for drone in self.drones:
            drone.update_state(effective_hours, consumption_multiplier=area_density_factor)

        active_drones = [d for d in self.drones if d.status != "DEPLETED"]
        total_dispensed = sum(d.dispensed_kg for d in self.drones)

        density_coverage = len(active_drones) / (self.area_sq_km / 500.0)
        coverage_factor = min(1.0, density_coverage)

        base_reduction = (total_dispensed / 50000.0) * 5.0 * coverage_factor

        half_life = self.profile["aerosol_half_life_hours"]
        decay = 0.5 ** (current_hour / half_life)
        simulated_reduction = base_reduction * decay

        efficiency = (simulated_reduction / self.desired_reduction_pct) * 100 if self.desired_reduction_pct > 0 else 0

        return {
            "target_region": self.target_region,
            "base_irradiance": self.profile["base_irradiance"],
            "total_drones": total_drones,
            "active_drones": len(active_drones),
            "total_dispensed_kg": round(total_dispensed, 2),
            "simulated_reduction": f"{simulated_reduction:.2f}%",
            "simulated_reduction_val": float(simulated_reduction),
            "efficiency": f"{min(efficiency, 100.0):.1f}%"
        }