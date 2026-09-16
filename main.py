import numpy as np
from src.drone import Drone
from src.simulator import ClimateSimulator
from src.database import DatabaseManager

def main():
    target_region = "Atacama"
    area_sq_km = 12000.0
    desired_reduction = 5.0
    drone_count = 25
    elapsed_hours = 6.0

    print(f"Initializing mission for region: {target_region}")
    print(f"Coverage Area: {area_sq_km} sq km | Target Reduction: {desired_reduction}%")

    sim = ClimateSimulator(
        target_region=target_region, 
        area_sq_km=area_sq_km, 
        desired_reduction_pct=desired_reduction
    )

    grid_size = int(np.ceil(np.sqrt(drone_count)))
    spacing = np.sqrt(area_sq_km) / grid_size

    np.random.seed(42)

    for i in range(drone_count):
        row = i // grid_size
        col = i % grid_size

        base_x = 100.0 + (col * spacing * 0.1)
        base_y = 50.0 + (row * spacing * 0.1)
        wind_drift_x = np.random.uniform(-0.4, 0.4)
        wind_drift_y = np.random.uniform(-0.4, 0.4)

        pos_x = base_x + wind_drift_x
        pos_y = base_y + wind_drift_y

        sim.add_drone(Drone(drone_id=i+1, position=(pos_x, pos_y), fuel=100.0, particle_capacity=3000.0))

    results = sim.run_simulation(current_hour=elapsed_hours)

    db = DatabaseManager()
    mission_id = db.save_mission(target_region, area_sq_km, desired_reduction)
    db.save_telemetry(mission_id, sim.drones)

    print("\nMission Execution Summary:")
    print(f"Mission ID: {mission_id}")
    print(f"Base Irradiance: {results.get('base_irradiance', 1000.0)} W/m2")
    print(f"Active Drones: {results['active_drones']} / {results['total_drones']}")
    print(f"Simulated Reduction: {results['simulated_reduction']}")
    print(f"Fleet Efficiency: {results['efficiency']}")
    print(f"Total Dispensed: {results['total_dispensed_kg']} kg")

if __name__ == "__main__":
    main()