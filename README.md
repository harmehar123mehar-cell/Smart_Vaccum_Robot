# SMARTBOT AI — Python Backend Edition

A 3D browser simulation with a Python AI engine. The browser is a visual client; search, target selection, fuzzy cleaning intensity, battery rules, learning updates, and persistence are handled by Python.

## Run on macOS / Windows / Linux

1. Install Python 3.10+.
2. Extract this folder.
3. Open a terminal in the `SMARTBOT_AI_Python` folder.
4. Create and activate a virtual environment:

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Start the backend:
```bash
python app.py
```

7. Open http://127.0.0.1:5000 in your browser.

Do not double-click the HTML file. Open the Flask URL so the frontend can call the Python API.

## Backend API
- `GET /api/health` — backend health
- `GET /api/state` — current simulation and knowledge state
- `POST /api/start` — start or resume; JSON `{"algorithm":"ASTAR"}`
- `POST /api/tick` — perform one AI simulation step
- `POST /api/pause` — pause
- `POST /api/new-session` — generate a new environment, retain learned memory
- `POST /api/algorithm` — change algorithm; `BFS`, `DFS`, `ASTAR`
- `POST /api/reset-memory` — clear SQLite memory and session history
- `GET /api/history` — recent session records

## AI concepts implemented
1. **Intelligent agent:** Python agent observes map, dirt, obstacles, battery, and stored knowledge; selects actions.
2. **Problem formulation:** grid states, legal actions, initial position, target locations, path cost.
3. **Uninformed search:** BFS and DFS.
4. **Informed search:** A* with Manhattan-distance heuristic.
5. **Knowledge representation:** SQLite facts for tile visits, dirty observations, and estimated dirt probability.
6. **Learning by induction:** repeated observations update each tile's dirt likelihood using smoothed frequency estimates. Learned locations can reappear in later environments and influence target selection.
7. **Probabilistic reasoning:** estimated dirt probability from observations.
8. **Fuzzy logic:** interpretable rule-based fuzzy-style weighted inference combines dirt level and battery level to select cleaning intensity.
9. **Expert system:** low battery triggers a return-to-dock rule; the robot uses A* to return and recharge.
10. **IoT-style telemetry:** simulated battery, sensor/environment state and status.

## What is simulated / limitations
- This is a software simulator, not a physical robot or real sensor integration.
- The fuzzy controller is a compact weighted fuzzy-rule inference demonstration, not a full industrial fuzzy-control package.
- The dirt probability is an experience-based estimate, not a trained neural network.
- SQLite database `smartbot.db` is created automatically beside `app.py`.
- Three.js is loaded from a CDN, so internet is needed for the 3D rendering library.
- Flask development server is intended for local demo, not public production hosting.

## Suggested viva explanation
"The frontend only visualises the environment. Every navigation and decision step is requested from a Flask API. The Python agent uses BFS, DFS or A* to find a path. It records observations in SQLite and updates dirt likelihood estimates. The learned estimates influence later target selection. A fuzzy rule system adjusts cleaning intensity, while an expert rule sends the robot to its charging dock when battery is critical."
