import sqlite3

class DatabaseManager:
    def __init__(self, db_name: str = "orbital_climate.db"):
        self.db_name = db_name
        self._create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS missions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_region TEXT NOT NULL,
                    area_sq_km REAL NOT NULL,
                    desired_reduction_pct REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mission_id INTEGER,
                    drone_id INTEGER NOT NULL,
                    position_x REAL NOT NULL,
                    position_y REAL NOT NULL,
                    fuel REAL NOT NULL,
                    particles_remaining REAL NOT NULL,
                    FOREIGN KEY (mission_id) REFERENCES missions (id)
                )
            """)
            conn.commit()

    def save_mission(self, target: str, area: float, reduction: float) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO missions (target_region, area_sq_km, desired_reduction_pct) VALUES (?, ?, ?)",
                (target, area, reduction)
            )
            conn.commit()
            return int(cursor.lastrowid or 0)

    def save_telemetry(self, mission_id: int, drones: list):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            telemetry_data = [
                (mission_id, d.drone_id, d.position[0], d.position[1], d.fuel, d.current_particles)
                for d in drones
            ]
            cursor.executemany("""
                INSERT INTO telemetry (mission_id, drone_id, position_x, position_y, fuel, particles_remaining)
                VALUES (?, ?, ?, ?, ?, ?)
            """, telemetry_data)
            conn.commit()