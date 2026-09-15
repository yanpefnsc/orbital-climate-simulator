class Drone:
    def __init__(self, drone_id: int, position: tuple[float, float], fuel: float, particle_capacity: float):
        self.drone_id = drone_id
        self.position = position
        self.fuel = fuel
        self.particle_capacity = particle_capacity
        self.current_particles = particle_capacity

    def status(self) -> dict:
        return {
            "id": self.drone_id,
            "position": self.position,
            "fuel": f"{self.fuel}%",
            "particles": self.current_particles
        }