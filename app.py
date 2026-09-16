import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import pandas as pd
from src.drone import Drone
from src.simulator import ClimateSimulator
from src.database import DatabaseManager

st.set_page_config(page_title="Orbital Climate Control Operations", layout="wide")
plt.style.use('dark_background')

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e6ed; }
    .hud-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
    .hud-title { font-size: 11px; text-transform: uppercase; color: #8b949e; margin-bottom: 4px; font-weight: 600; }
    .hud-value { font-size: 20px; font-weight: bold; color: #00d2ff; }
    .hud-sub { font-size: 11px; color: #ff9900; }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ Orbital Aerosol Climate Control System")
st.markdown("Avionic telemetry dashboard for Solar Radiation Management (SRM) operations.")

db = DatabaseManager()

if 'elapsed_hours' not in st.session_state:
    st.session_state.elapsed_hours = 1.5

if 'sim' not in st.session_state:
    st.session_state.sim = None

if 'refuel_message' not in st.session_state:
    st.session_state.refuel_message = False

def acionar_refuel():
    if st.session_state.sim is not None:
        st.session_state.sim.refuel_fleet()
        st.session_state.elapsed_hours = 0.5
        st.session_state.refuel_message = True

st.sidebar.header("Mission Parameters")
target_region = st.sidebar.text_input("Target Region", "Atacama")
area_sq_km = st.sidebar.number_input("Coverage Area (sq km)", min_value=1000.0, max_value=100000.0, value=10000.0, step=1000.0)
desired_reduction = st.sidebar.slider("Target Solar Reduction (%)", 0.1, 20.0, 5.0, 0.1, format="%.1f%%")
drone_count = st.sidebar.slider("Drone Fleet Size", 5, 100, 50)

st.sidebar.subheader("Simulation Control")
elapsed_hours = st.sidebar.slider("Mission Elapsed Time (Hours)", 0.5, 24.0, key="elapsed_hours", step=0.5)

if st.sidebar.button("Execute Operations"):
    sim = ClimateSimulator(target_region=target_region, area_sq_km=area_sq_km, desired_reduction_pct=desired_reduction)
    grid_size = int(np.ceil(np.sqrt(drone_count)))
    spacing = np.sqrt(area_sq_km) / grid_size
    np.random.seed(42)

    for i in range(drone_count):
        row, col = i // grid_size, i % grid_size
        pos_x = 100.0 + (col * spacing * 0.1) + np.random.uniform(-0.4, 0.4)
        pos_y = 50.0 + (row * spacing * 0.1) + np.random.uniform(-0.4, 0.4)
        sim.add_drone(Drone(drone_id=i+1, position=(pos_x, pos_y), fuel=100.0, particle_capacity=3000.0))

    st.session_state.sim = sim

st.sidebar.subheader("Maintenance Control")
st.sidebar.button("🔄 Return & Refuel Fleet", on_click=acionar_refuel)

if st.session_state.refuel_message:
    st.sidebar.success("Fleet fully refueled!")
    st.session_state.refuel_message = False

if st.session_state.sim is not None:
    sim = st.session_state.sim

    results_24h = sim.run_simulation(current_hour=24.0)
    results = sim.run_simulation(current_hour=elapsed_hours)

    mission_id = db.save_mission(target_region, area_sq_km, desired_reduction)
    db.save_telemetry(mission_id, sim.drones)

    achieved_red_val = results["simulated_reduction_val"]
    final_red_val_24h = results_24h["simulated_reduction_val"]
    base_irradiance = results.get("base_irradiance", 1280.0)
    current_irradiance = base_irradiance * (1.0 - (achieved_red_val / 100.0))
    final_irradiance_24h = base_irradiance * (1.0 - (final_red_val_24h / 100.0))
    target_irradiance = base_irradiance * (1.0 - (desired_reduction / 100.0))

    grid_size = int(np.ceil(np.sqrt(drone_count)))
    spacing = np.sqrt(area_sq_km) / grid_size

    main_col, right_hud = st.columns([7.5, 2.5])

    with main_col:
        st.subheader("Orbital Telemetry & Spatial Coverage")
        c1, c2 = st.columns(2)

        with c1:
            x_coords = [d.position[0] for d in sim.drones]
            y_coords = [d.position[1] for d in sim.drones]

            fig, ax = plt.subplots(figsize=(5, 3.8))
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')

            for x, y in zip(x_coords, y_coords):
                ax.add_patch(Circle((x, y), radius=2.0, color='cyan', alpha=0.15, zorder=1))

            statuses = [d.status for d in sim.drones]
            colors = ['#00ffcc' if s == 'NOMINAL' else ('#ffcc00' if s == 'LOW_FUEL' else '#ff3366') for s in statuses]
            ax.scatter(x_coords, y_coords, color=colors, edgecolors='#ffffff', linewidths=0.8, s=45, zorder=3)

            ax.set_title(f"2D Mesh Grid ({target_region.title()})", color='#ffffff', fontsize=10)
            ax.tick_params(colors='#a0a0a0', labelsize=8)
            ax.grid(True, linestyle=':', alpha=0.3, color='#444444')
            st.pyplot(fig)

        with c2:
            hours_timeline = np.linspace(0, 24, 100)
            drop_range = base_irradiance - (base_irradiance * (achieved_red_val / 100.0))
            sigmoid_decay = 1 / (1 + np.exp(-1.5 * (hours_timeline - (elapsed_hours / 2.0))))
            irradiance_curve = base_irradiance - (drop_range * sigmoid_decay)

            fig2, ax2 = plt.subplots(figsize=(5, 3.8))
            fig2.patch.set_facecolor('#0e1117')
            ax2.set_facecolor('#0e1117')

            ax2.plot(hours_timeline, irradiance_curve, color='#ff9900', linewidth=2)
            ax2.axhline(y=target_irradiance, color='#ff3366', linestyle='--')
            ax2.axvline(x=elapsed_hours, color='#00d2ff', linestyle=':')

            ax2.set_title("Irradiance Attenuation Timeline", color='#ffffff', fontsize=10)
            ax2.tick_params(colors='#a0a0a0', labelsize=8)
            ax2.grid(True, linestyle=':', alpha=0.3, color='#444444')
            st.pyplot(fig2)

        st.subheader("Fleet Telemetry Logs")
        df_telemetry = pd.DataFrame([d.get_dict() for d in sim.drones])
        st.dataframe(df_telemetry, use_container_width=True, height=200)

    with right_hud:
        st.subheader("Mission HUD")

        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Mission ID</div>
            <div class="hud-value">#{mission_id}</div>
            <div class="hud-sub">Region: {target_region.title()}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Solar Reduction</div>
            <div class="hud-value">{results['simulated_reduction']}</div>
            <div class="hud-sub">Target Goal: {desired_reduction:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Irradiance (Current / Final)</div>
            <div class="hud-value">{current_irradiance:.1f} W/m²</div>
            <div class="hud-sub">Final at 24h: <b>{final_irradiance_24h:.1f} W/m²</b> (Base: {base_irradiance:.1f})</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Fleet Efficiency</div>
            <div class="hud-value">{results['efficiency']}</div>
            <div class="hud-sub">Active: {results['active_drones']} / {results['total_drones']} Units</div>
        </div>
        """, unsafe_allow_html=True)

        nominal_count = sum(1 for d in sim.drones if d.status == 'NOMINAL')
        low_fuel_count = sum(1 for d in sim.drones if d.status == 'LOW_FUEL')
        depleted_count = sum(1 for d in sim.drones if d.status == 'DEPLETED')

        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">System Status</div>
            <div style="font-size:12px; margin-top:4px;">
                🟢 <b>Nominal:</b> {nominal_count}<br>
                🟡 <b>Low Fuel:</b> {low_fuel_count}<br>
                🔴 <b>Depleted:</b> {depleted_count}
            </div>
        </div>
        """, unsafe_allow_html=True)

        csv_data = df_telemetry.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Telemetry CSV",
            data=csv_data,
            file_name=f"mission_{mission_id}_telemetry.csv",
            mime="text/csv",
            width='stretch'
        )