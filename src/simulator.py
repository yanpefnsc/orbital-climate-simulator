from src.drone import Drone

class ClimateSimulator:
    def __init__(self, target_region: str, area_sq_km: float, desired_reduction_pct: float):
        self.target_region = target_region
        self.area_sq_km = area_sq_km
        self.desired_reduction_pct = desired_reduction_pct
        self.drones: list[Drone] = []

    def add_drone(self, drone: Drone):
        self.drones.append(drone)

    def run_simulation(self) -> dict:
        num_drones = len(self.drones)
        if num_drones == 0:
            return {"error": "Nenhum drone na frota."}

        total_capacity = sum(d.current_particles for d in self.drones)
        simulated_reduction = min(self.desired_reduction_pct, (total_capacity / (self.area_sq_km * 10)) * 100)
        estimated_loss = 8.5
        efficiency = round((simulated_reduction / self.desired_reduction_pct) * 100, 2) if self.desired_reduction_pct > 0 else 0

        return {
            "target": self.target_region,
            "area_sq_km": self.area_sq_km,
            "desired_reduction": f"{self.desired_reduction_pct}%",
            "simulated_reduction": f"{round(simulated_reduction, 2)}%",
            "active_drones": num_drones,
            "particle_loss": f"{estimated_loss}%",
            "efficiency": f"{efficiency}%",
            "status": "✓ Alvo atingido" if simulated_reduction >= self.desired_reduction_pct else "⚠ Capacidade insuficiente"
        }