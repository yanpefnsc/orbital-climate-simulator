from src.drone import Drone
from src.simulator import ClimateSimulator
from src.visualizer import SimulationVisualizer

def main():
    sim = ClimateSimulator(target_region="São Paulo", area_sq_km=10000.0, desired_reduction_pct=5.0)

    for i in range(1, 21):
        sim.add_drone(Drone(drone_id=i, position=(100.0 + (i * 2), 50.0 + (i * 1.5)), fuel=100.0, particle_capacity=3000.0))

    results = sim.run_simulation()

    print("\n════════ SIMULAÇÃO V2 ════════")
    for key, value in results.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("═══════════════════════════════\n")

    
    hours = [0, 1, 2, 3, 4, 5, 6]
    radiation_levels = [100.0, 99.1, 98.0, 96.8, 95.9, 95.3, 95.3]

    print("Gerando gráficos...")
    SimulationVisualizer.plot_drone_positions(sim.drones)
    SimulationVisualizer.plot_radiation_reduction(hours, radiation_levels)

if __name__ == "__main__":
    main()