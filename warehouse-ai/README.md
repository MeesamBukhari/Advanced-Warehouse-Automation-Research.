# 🛰️ WAREHOUSE.AI // TACTICAL SIMULATOR

A professional-grade AI simulation platform designed to benchmark pathfinding algorithms and intelligent agent behavior in complex warehouse environments. Built with a high-fidelity "Cyber-Tactical" HUD for real-time telemetry and performance analytics.

## 🚀 Key Features

### 🧠 Advanced Search Suite
Explore a wide range of pathfinding strategies:
- **Informed Search**: A* (with dynamic heuristic weighting), Greedy Best-First Search.
- **Uninformed Search**: BFS, DFS, UCS (Uniform Cost).
- **Local Search**: Hill Climbing optimization.
- **Adversarial Search**: Minimax with Alpha-Beta Pruning for competitive scenarios.

### 🤖 Intelligent Agent Framework
Four distinct models of machine intelligence:
- **Reflex Agent**: Reactive decision-making based on immediate percepts.
- **Model-Based Agent**: Maintains an internal memory map of visited terrain.
- **Goal-Based Agent**: Long-term strategic planning to reach targets.
- **Utility-Based Agent**: Optimizes movement to maximize efficiency across multiple goals.

### 📊 Performance Analytics
- **Live HUD**: Real-time animation of robot movement and state exploration.
- **Comparison Dashboard**: Side-by-side interactive charts (Latency vs. Space Complexity).
- **Data Export**: Mission history archival with CSV export capabilities.
- **Runtime Controls**: Live adjustment of sensor FPS, search depth, and heuristic bias.

## 📦 Installation

1. **Clone the repository** (or navigate to the project folder).
2. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. **Launch the platform**:
   ```bash
   python -m streamlit run app.py
   ```

## 📂 Directory Structure

```text
warehouse-ai/
├── app.py                # Streamlit Entry Point & HUD
├── requirements.txt      # Project Dependencies
├── environment/
│   └── warehouse_grid.py # Logic for grid, occupancy, and state
├── algorithms/           # Search Logic Modules
│   ├── astar.py
│   ├── bfs.py
│   ├── minimax.py (Alpha-Beta Pruning)
│   └── ... 
├── agents/               # Intelligent Agent Models
│   ├── reflex_agent.py
│   └── ...
└── scenarios/            # Library of 10+ Scenario JSONs
```

## 🛰️ UI Aesthetics
The interface uses a custom **Tactical-HUD CSS** design featuring:
- **Pulsating Neon Glows** for active entities.
- **Scanline Filters** and Dot-Matrix backgrounds.
- **Clean Monospace Typography** for telemetry data.

## 🛠️ Built With
- **Python 3.13**
- **Streamlit** (Web HUD)
- **Plotly & Matplotlib** (Data Analysis)
- **Pandas** (Logging & Matrix Comparison)

