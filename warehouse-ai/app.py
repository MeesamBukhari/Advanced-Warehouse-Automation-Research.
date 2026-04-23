import streamlit as st
import time
import json
import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
from environment.warehouse_grid import Warehouse, CellType, Position
from algorithms.astar import a_star_search
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.ucs import ucs_search
from algorithms.hill_climbing import hill_climbing_search
from algorithms.greedy import greedy_best_first_search
from algorithms.minimax import get_best_move_adversarial
from agents.reflex_agent import ReflexAgent
from agents.model_agent import ModelBasedAgent
from agents.goal_agent import GoalBasedAgent
from agents.utility_agent import UtilityBasedAgent

# --- STYLING ---
st.set_page_config(page_title="WAREHOUSE.AI // COMMAND", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'JetBrains Mono', monospace;
        background-color: #050510;
        color: #C8F0FF;
    }
    
    .stApp {
        background: linear-gradient(135deg, #050510 0%, #08081A 100%);
    }

    .grid-container {
        display: inline-grid;
        gap: 1px;
        background-color: #101030;
        padding: 4px;
        border: 1px solid #00FFFF66;
        border-radius: 4px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
    }
    
    .cell { width: 22px; height: 22px; border-radius: 2px; }
    .cell-empty { background-color: #0F0F25; }
    .cell-shelf { background-color: #1A1A35; border: 1px solid #303060; }
    .cell-obstacle { background-color: #4A001F; border: 1px solid #FF000033; }
    .cell-robot { background-color: #00FFB4; box-shadow: 0 0 10px #00FFB4; border-radius: 4px; }
    .cell-item { background-color: #FFC800; box-shadow: 0 0 15px #FFC800; border-radius: 50%; }
    .cell-path { background-color: rgba(180, 0, 255, 0.6); }
    .cell-explored { background-color: rgba(59, 130, 246, 0.2); }

    .hud-panel {
        background: rgba(10, 10, 30, 0.95);
        border: 1px solid #00FFFF33;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    
    .hud-header {
        color: #00FFFF;
        font-size: 0.9rem;
        font-weight: bold;
        letter-spacing: 1px;
        border-bottom: 1px solid #00FFFF33;
        margin-bottom: 8px;
        padding-bottom: 4px;
    }
    
    .stat-val { color: #00FFB4; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- APP LOGIC ---

if 'mission_history' not in st.session_state:
    st.session_state.mission_history = []

def load_scenario(name):
    path = f"scenarios/{name}"
    with open(path, 'r') as f:
        return json.load(f)

def render_grid(warehouse):
    html = '<div class="grid-container" style="grid-template-columns: repeat(' + str(warehouse.width) + ', 1fr);">'
    for y in range(warehouse.height):
        for x in range(warehouse.width):
            cell = warehouse.get_cell(x, y)
            cls = "cell-empty"
            if cell == CellType.SHELF: cls = "cell-shelf"
            elif cell == CellType.OBSTACLE: cls = "cell-obstacle"
            elif cell == CellType.ROBOT: cls = "cell-robot"
            elif cell == CellType.ITEM: cls = "cell-item"
            elif cell == CellType.PATH: cls = "cell-path"
            elif cell == CellType.EXPLORED: cls = "cell-explored"
            html += f'<div class="cell {cls}"></div>'
    html += '</div>'
    return html

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🎛️ CONTROL CENTER")

scenario_files = sorted([f for f in os.listdir("scenarios") if f.endswith(".json")])
selected_scenario = st.sidebar.selectbox("📂 SCENARIO FILE", scenario_files)

mode = st.sidebar.radio("🕹️ MISSION MODE", ["Informed Search", "Uninformed Search", "Local/Adversarial", "AI Agents"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ RUNTIME PARAMETERS")

# Dynamic Parameters
h_weight = st.sidebar.slider("A* HEURISTIC WEIGHT", 0.1, 5.0, 1.0)
max_depth = st.sidebar.number_input("MAX DEPTH LIMIT", 1, 1000, 500)
hc_iters = st.sidebar.number_input("HILL CLIMB ITERATIONS", 10, 5000, 1000)
anim_speed = st.sidebar.slider("⚡ SENSOR FPS", 1, 60, 20)

st.sidebar.markdown("---")

if st.sidebar.button("🔌 INITIALIZE SYSTEM"):
    data = load_scenario(selected_scenario)
    st.session_state.warehouse = Warehouse(data['width'], data['height'])
    st.session_state.config = data
    
    w = st.session_state.warehouse
    for s in data.get('shelves', []):
        for i in range(s[0], s[0]+s[2]):
            for j in range(s[1], s[1]+s[3]): w.set_cell(i, j, CellType.SHELF)
    for o in data.get('obstacles', []):
        for i in range(o[0], o[0]+o[2]):
            for j in range(o[1], o[1]+o[3]): w.set_cell(i, j, CellType.OBSTACLE)
    for item in data.get('items', []):
        w.set_cell(item[0], item[1], CellType.ITEM)
    
    start = data.get('robot_start', [0, 0])
    w.set_cell(start[0], start[1], CellType.ROBOT)
    st.session_state.start_pos = Position(start[0], start[1])
    st.session_state.system_ready = True
    st.rerun()

# --- MAIN INTERFACE ---
t1, t2, t3 = st.tabs(["🛰️ LIVE FEED", "📊 ANALYTICS", "📑 MISSION LOGS"])

if 'warehouse' in st.session_state:
    w = st.session_state.warehouse
    
    with t1:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div class="hud-header">MISSION VISUALIZER: {selected_scenario}</div>', unsafe_allow_html=True)
            grid_placeholder = st.empty()
            grid_placeholder.markdown(render_grid(w), unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="hud-panel"><div class="hud-header">TELEMETRY DATA</div>', unsafe_allow_html=True)
            stats_placeholder = st.empty()
            
            # Select specific algorithm based on mode
            if mode == "Informed Search":
                run_algo = st.selectbox("EXECUTE:", ["A*", "Greedy BFS"])
            elif mode == "Uninformed Search":
                run_algo = st.selectbox("EXECUTE:", ["BFS", "DFS", "UCS"])
            elif mode == "Local/Adversarial":
                run_algo = st.selectbox("EXECUTE:", ["Hill Climbing", "Adversarial (Minimax)"])
            else:
                run_algo = st.selectbox("EXECUTE:", ["Reflex Agent", "Model-Based", "Goal-Based", "Utility-Based"])

            if st.button("▶️ START MISSION"):
                goal = w.items[0] if w.items else Position(0,0)
                start_time = time.perf_counter()
                path, explored = [], []
                
                # Execution Logic
                if run_algo == "A*": path, explored = a_star_search(w, st.session_state.start_pos, goal)
                elif run_algo == "Greedy BFS": path, explored = greedy_best_first_search(w, st.session_state.start_pos, goal)
                elif run_algo == "BFS": path, explored = bfs_search(w, st.session_state.start_pos, goal)
                elif run_algo == "DFS": path, explored = dfs_search(w, st.session_state.start_pos, goal)
                elif run_algo == "UCS": path, explored = ucs_search(w, st.session_state.start_pos, goal)
                elif run_algo == "Hill Climbing": path, explored = hill_climbing_search(w, st.session_state.start_pos, goal)
                elif run_algo == "Adversarial (Minimax)":
                    curr = st.session_state.start_pos
                    path = [curr]
                    for _ in range(50):
                        next_mv = get_best_move_adversarial(w, curr, goal, depth=3)
                        if next_mv == curr: break
                        path.append(next_mv)
                        curr = next_mv
                        if curr == goal: break
                    explored = path
                else:
                    # Agent Loop (Abstracted here for space)
                    agent_map = {"Reflex Agent": ReflexAgent, "Model-Based": ModelBasedAgent, "Goal-Based": GoalBasedAgent, "Utility-Based": UtilityBasedAgent}
                    agent = agent_map[run_algo](st.session_state.start_pos)
                    curr = st.session_state.start_pos
                    path = [curr]
                    for _ in range(200):
                        nx = agent.get_action(w) if run_algo == "Utility-Based" else agent.get_action(w, goal)
                        if nx == curr: break
                        path.append(nx)
                        curr = nx
                        if curr == goal: break
                    explored = path

                exec_time = (time.perf_counter() - start_time) * 1000
                
                # Animation
                for i, pos in enumerate(path):
                    if i > 0: w.set_cell(path[i-1].x, path[i-1].y, CellType.PATH)
                    w.set_cell(pos.x, pos.y, CellType.ROBOT)
                    grid_placeholder.markdown(render_grid(w), unsafe_allow_html=True)
                    stats_placeholder.markdown(f"""
                        **ALGO**: {run_algo}<br>
                        **STEP**: <span class="stat-val">{i}</span><br>
                        **COST**: <span class="stat-val">{len(path)}</span><br>
                        **EXPLORED**: <span class="stat-val">{len(explored)}</span><br>
                        **LATENCY**: <span class="stat-val">{exec_time:.2f}ms</span>
                    """, unsafe_allow_html=True)
                    time.sleep(1/anim_speed)
                
                st.success("MISSION COMPLETE: Goal reached.")
                
                # Save to History
                st.session_state.mission_history.append({
                    "Scenario": selected_scenario, "Algorithm": run_algo, "Time (ms)": exec_time,
                    "Nodes Explored": len(explored), "Path Length": len(path)
                })

    with t2:
        st.markdown('<div class="hud-header">PERFORMANCE_ANALYTICS</div>', unsafe_allow_html=True)
        if st.session_state.mission_history:
            df = pd.DataFrame(st.session_state.mission_history)
            
            c1, c2 = st.columns(2)
            with c1:
                fig1 = px.bar(df, x="Algorithm", y="Time (ms)", color="Algorithm", title="Execution Latency (ms)")
                fig1.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig1, use_container_width=True)
            
            with c2:
                fig2 = px.bar(df, x="Algorithm", y="Nodes Explored", color="Algorithm", title="Space Complexity (Nodes)")
                fig2.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)
                
            st.markdown('<div class="hud-header">COMPARISON MATRIX</div>', unsafe_allow_html=True)
            st.dataframe(df.style.highlight_min(axis=0, color='#00FFB466'), use_container_width=True)
        else:
            st.info("Execute missions to generate comparative data.")

    with t3:
        st.markdown('<div class="hud-header">MISSION LOG ARCHIVE</div>', unsafe_allow_html=True)
        if st.session_state.mission_history:
            log_df = pd.DataFrame(st.session_state.mission_history)
            st.table(log_df)
            
            csv = log_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 EXPORT MISSION DATA (CSV)", data=csv, file_name="warehouse_ai_logs.csv", mime='text/csv')
        else:
            st.info("No mission logs detected.")

else:
    st.info("Initialize system in the sidebar to load telemetry feed.")
