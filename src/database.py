import sqlite3

class DatabaseManager:
    def __init__(self, db_path="orbital_climate.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_region TEXT,
                area_sq_km REAL,
                desired_reduction REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_id INTEGER,
                drone_id INTEGER,
                pos_x REAL,
                pos_y REAL,
                fuel_pct REAL,
                dispensed_kg REAL,
                status TEXT,
                FOREIGN KEY (mission_id) REFERENCES missions (id)
            )
        """)
        
        conn.commit()
        conn.close()

    def save_mission(self, target_region, area_sq_km, desired_reduction):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO missions (target_region, area_sq_km, desired_reduction)
            VALUES (?, ?, ?)
        """, (target_region, area_sq_km, desired_reduction))
        mission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return mission_id

    def save_telemetry(self, mission_id, drones):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for drone in drones:
            d_dict = drone.get_dict()
            cursor.execute("""
                INSERT INTO telemetry (mission_id, drone_id, pos_x, pos_y, fuel_pct, dispensed_kg, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                mission_id,
                d_dict["drone_id"],
                d_dict["x"],
                d_dict["y"],
                d_dict["fuel_pct"],
                d_dict["dispensed_kg"],
                d_dict["status"]
            ))
        conn.commit()
        conn.close()

    def get_latest_telemetry(self, mission_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT drone_id, pos_x, pos_y, fuel_pct, dispensed_kg, status
            FROM telemetry
            WHERE mission_id = ?
        """, (mission_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows