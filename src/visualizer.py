import matplotlib.pyplot as plt

class SimulationVisualizer:
    @staticmethod
    def plot_drone_positions(drones: list):
        x_coords = [d.position[0] for d in drones]
        y_coords = [d.position[1] for d in drones]

        plt.figure(figsize=(8, 6))
        plt.scatter(x_coords, y_coords, color='cyan', edgecolors='blue', s=100, label='Orbital Drones')
        plt.title('Orbital Drone Fleet Formation')
        plt.xlabel('X Coordinate (km)')
        plt.ylabel('Y Coordinate (km)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_radiation_reduction(hours: list[int], radiation_levels: list[float]):
        plt.figure(figsize=(8, 4))
        plt.plot(hours, radiation_levels, marker='o', color='orange', linewidth=2, label='Radiation Level (%)')
        plt.title('Regional Solar Attenuation Over Time')
        plt.xlabel('Operation Time (Hours)')
        plt.ylabel('Received Solar Radiation (%)')
        plt.axhline(y=95, color='r', linestyle=':', label='Target (95%)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()