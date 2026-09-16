# Orbital Climate Simulator

> An interactive mission-control dashboard for exploring the operational trade-offs of a conceptual Solar Radiation Management (SRM) drone fleet.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-mission%20data-003B57?logo=sqlite&logoColor=white)

## Why this project?

Climate interventions are often discussed at a global scale, but their execution is an operations problem: **How large is the coverage area? How many units are active? How does fuel availability affect the mission? What happens as aerosols dissipate?**

**Orbital Climate Simulator** turns those questions into an interactive, visual experiment. It models a fictional fleet of atmospheric drones that disperses reflective particles and presents the outcome in a mission-control interface.

This is a portfolio project that combines simulation logic, data persistence and data visualization in a focused product experience.

> **Important:** This is an educational, conceptual simulator - not a scientific climate model and not a recommendation for real-world geoengineering.

## What you can explore

- Configure the target region, coverage area and solar-reduction objective.
- Deploy a fleet of 5-100 simulated drones in a spatial mesh.
- Track fuel, particle dispersion and the operational state of every unit.
- Compare the desired solar-radiation reduction with the simulated result.
- Visualize coverage, irradiance attenuation over time and fleet telemetry.
- Refill the fleet and export a mission telemetry report as CSV.
- Store mission parameters and telemetry records in SQLite.

## How the simulation works

The simulator applies a deliberately simplified operational model:

1. A mission is configured with a region, area, target reduction and fleet size.
2. Drones are distributed over a 2D grid and consume fuel while dispensing particles.
3. Coverage depends on the number of active drones relative to the area.
4. Regional profiles adjust baseline irradiance, wind factor and aerosol half-life.
5. The displayed solar-radiation reduction is calculated from total dispersed mass, coverage and aerosol decay.

The goal is not physical accuracy; it is to make the relationships between fleet capacity, area, time and operational constraints intuitive and inspectable.

## Technology

| Layer | Tools |
| --- | --- |
| Interface | Streamlit |
| Visualization | Matplotlib |
| Numerical/data handling | NumPy and pandas |
| Persistence | SQLite |
| Language | Python |

## Architecture

```text
app.py                 Streamlit mission-control dashboard
src/
  drone.py             Drone state, fuel consumption and particle dispensing
  simulator.py         Regional profiles and simulation calculations
  database.py          SQLite mission and telemetry persistence
orbital_climate.db     Local simulation database
```

## Run locally

```bash
git clone https://github.com/yanpefnsc/orbital-climate-simulator.git
cd orbital-climate-simulator
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install the dependencies and start the dashboard:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit, configure the mission in the sidebar and select **Execute Operations**.


## Author

Built by [Yan Pefnsc](https://github.com/yanpefnsc).

If you found this project interesting, feel free to star the repository or open an issue with feedback.
