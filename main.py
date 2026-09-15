from src.drone import Drone
from src.simulator import ClimateSimulator

def main():
    sim = ClimateSimulator(target_region="São Paulo", area_sq_km=10000.0, desired_reduction_pct=5.0)

    for i in range(1, 21):
        sim.add_drone(Drone(drone_id=i, position=(100.0 + i, 50.0 + i), fuel=100.0, particle_capacity=3000.0))

    results = sim.run_simulation()

    print("\n════════ SIMULAÇÃO V1 ════════")
    for key, value in results.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("═══════════════════════════════\n")

if __name__ == "__main__":
    main()