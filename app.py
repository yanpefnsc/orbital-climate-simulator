import streamlit as st
import matplotlib.pyplot as plt
from src.drone import Drone
from src.simulator import ClimateSimulator
from src.database import DatabaseManager

st.set_page_config(page_title="Orbital Climate Simulator", layout="wide")

st.title("🛰️ Orbital Aerosol Climate Control Simulator")
st.markdown("Interactive interface for mission planning and orbital fleet management.")

db = DatabaseManager()

st.sidebar.header("Mission Parameters")
target_region = st.sidebar.text_input("Target Region", "Sao Paulo")
area_sq_km = st.sidebar.number_input("Coverage Area (sq km)", min_value=1000.0, max_value=100000.0, value=10000.0, step=1000.0)
desired_reduction = st.sidebar.slider("Target Solar Reduction (%)", min_value=1.0, max_value=20.0, value=5.0)
drone_count = st.sidebar.slider("Drone Count", min_value=5, max_value=100, value=20)

if st.sidebar.button("Run Simulation"):
    sim = ClimateSimulator(target_region=target_region, area_sq_km=area_sq_km, desired_reduction_pct=desired_reduction)
    
    for i in range(1, drone_count + 1):
        sim.add_drone(Drone(drone_id=i, position=(100.0 + (i * 2), 50.0 + (i * 1.5)), fuel=100.0, particle_capacity=3000.0))
        
    results = sim.run_simulation()
    
    mission_id = db.save_mission(target_region, area_sq_km, desired_reduction)
    db.save_telemetry(mission_id, sim.drones)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registered Mission", f"#{mission_id}")
    col2.metric("Active Drones", results["active_drones"])
    col3.metric("Simulated Reduction", results["simulated_reduction"])
    col4.metric("Efficiency", results["efficiency"])

    st.subheader("Orbital Formation & Telemetry")
    c1, c2 = st.columns(2)
    
    with c1:
        x_coords = [d.position[0] for d in sim.drones]
        y_coords = [d.position[1] for d in sim.drones]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(x_coords, y_coords, color='cyan', edgecolors='blue', s=80)
        ax.set_title("Orbital Drone Formation")
        ax.set_xlabel("X Coordinate (km)")
        ax.set_ylabel("Y Coordinate (km)")
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
        
    with c2:
        hours = [0, 1, 2, 3, 4, 5, 6]
        radiation = [100.0, 99.1, 98.0, 96.8, 95.9, 95.3, 95.3]
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.plot(hours, radiation, marker='o', color='orange', linewidth=2)
        ax2.axhline(y=100 - desired_reduction, color='r', linestyle=':', label='Target')
        ax2.set_title("Regional Solar Attenuation")
        ax2.set_xlabel("Time (Hours)")
        ax2.set_ylabel("Received Solar Radiation (%)")
        ax2.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig2)