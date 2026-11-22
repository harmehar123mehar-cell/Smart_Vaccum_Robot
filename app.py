from flask import Flask, jsonify, request, render_template
from collections import deque
import heapq
import sqlite3
import json
import os
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smartbot.db")
app = Flask(__name__)

WIDTH, HEIGHT = 8, 6
DOCK = (0, 0)
OBSTACLES = {(2, 1), (2, 2), (5, 1), (5, 2), (3, 4), (4, 4)}
BASE_DIRT = [(1, 0), (3, 0), (6, 0), (0, 2), (3, 2), (6, 2),
             (1, 3), (4, 3), (7, 3), (0, 5), (5, 5), (7, 5)]

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            algorithm TEXT,
            cleaned INTEGER DEFAULT 0,
            steps INTEGER DEFAULT 0,
            energy_used REAL DEFAULT 0,
            status TEXT DEFAULT 'active'
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS location_memory(
            x INTEGER NOT NULL, y INTEGER NOT NULL,
            dirty_observations INTEGER DEFAULT 0,
            visits INTEGER DEFAULT 0,
            dirt_probability REAL DEFAULT 0.15,
            PRIMARY KEY(x,y)
        )""")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) not in OBSTACLES:
                    con.execute("""INSERT OR IGNORE INTO location_memory
                    (x,y,dirty_observations,visits,dirt_probability)
                    VALUES(?,?,0,0,0.15)""", (x, y))

init_db()

# The active simulation is held server-side. Persistent learning lives in SQLite.
STATE = {}

def memory_rows():
    with db() as con:
        rows = con.execute("SELECT * FROM location_memory").fetchall()
    return {(r["x"], r["y"]): dict(r) for r in rows}

def save_observation(pos, was_dirty):
    x, y = pos
    with db() as con:
        row = con.execute("SELECT * FROM location_memory WHERE x=? AND y=?", (x,y)).fetchone()
        if row:
            visits = row["visits"] + 1
            dirty = row["dirty_observations"] + (1 if was_dirty else 0)
            # Beta-style smoothing avoids overconfidence with very few observations.
            probability = (dirty + 1.0) / (visits + 2.0)
            con.execute("""UPDATE location_memory SET visits=?, dirty_observations=?,
                        dirt_probability=? WHERE x=? AND y=?""",
                        (visits, dirty, probability, x, y))

def get_session_count():
    with db() as con:
        return con.execute("SELECT COUNT(*) FROM sessions WHERE status='completed'").fetchone()[0]

def new_session_record(algorithm):
    with db() as con:
        cur = con.execute("INSERT INTO sessions(started_at,algorithm,status) VALUES(?,?,?)",
                          (datetime.now().isoformat(timespec="seconds"), algorithm, "active"))
        return cur.lastrowid

def finish_session():
    sid = STATE.get("session_id")
    if not sid:
        return
    with db() as con:
        con.execute("""UPDATE sessions SET completed_at=?, cleaned=?, steps=?,
                    energy_used=?, status='completed' WHERE id=?""",
                    (datetime.now().isoformat(timespec="seconds"), STATE["cleaned"],
                     STATE["steps"], STATE["energy_used"], sid))

def valid(p):
    x, y = p
    return 0 <= x < WIDTH and 0 <= y < HEIGHT and p not in OBSTACLES

def neighbors(p):
    x, y = p
    # Fixed order makes the search reproducible.
    candidates = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
    return [q for q in candidates if valid(q)]

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def reconstruct(parent, node):
    path = [node]
    while node in parent:
        node = parent[node]
        path.append(node)
    return list(reversed(path))

def bfs(start, goal):
    queue = deque([start])
    parent, seen = {}, {start}
    expanded = 0
    while queue:
        cur = queue.popleft()
        expanded += 1
        if cur == goal:
            return reconstruct(parent, cur), expanded
        for nxt in neighbors(cur):
            if nxt not in seen:
                seen.add(nxt)
                parent[nxt] = cur
                queue.append(nxt)
    return [], expanded

def dfs(start, goal):
    stack = [start]
    parent, seen = {}, {start}
    expanded = 0
    while stack:
        cur = stack.pop()
        expanded += 1
        if cur == goal:
            return reconstruct(parent, cur), expanded
        # Reverse so visual traversal order remains consistent.
        for nxt in reversed(neighbors(cur)):
            if nxt not in seen:
                seen.add(nxt)
                parent[nxt] = cur
                stack.append(nxt)
    return [], expanded

def astar(start, goal):
    frontier = [(heuristic(start, goal), 0, start)]
    parent, cost = {}, {start: 0}
    expanded = 0
    while frontier:
        _, g, cur = heapq.heappop(frontier)
        if g != cost.get(cur):
            continue
        expanded += 1
        if cur == goal:
            return reconstruct(parent, cur), expanded
        for nxt in neighbors(cur):
            new_g = g + 1
            if new_g < cost.get(nxt, float("inf")):
                cost[nxt] = new_g
                parent[nxt] = cur
                heapq.heappush(frontier, (new_g + heuristic(nxt, goal), new_g, nxt))
    return [], expanded

SEARCH = {"BFS": bfs, "DFS": dfs, "ASTAR": astar}

def fuzzy_cleaning_intensity(dirt_level, battery):
    """Small Mamdani-style rule system with interpretable weighted rules."""
    # Inputs are normalised to [0,1]. Output is a cleaning intensity [0,1].
    low_battery = max(0.0, min(1.0, (35.0 - battery) / 30.0))
    high_dirt = max(0.0, min(1.0, (dirt_level - 0.25) / 0.65))
    medium_dirt = max(0.0, 1.0 - abs(dirt_level - 0.5) / 0.35)
    # Rules: high dirt -> strong; medium dirt -> normal; low battery -> conserve.
    strong = high_dirt * (1.0 - low_battery)
    normal = medium_dirt * (1.0 - 0.6 * low_battery)
    conserve = max(low_battery, 1.0 - high_dirt)
    numerator = strong * 0.95 + normal * 0.65 + conserve * 0.25
    denominator = strong + normal + conserve
    return round(numerator / denominator, 2) if denominator else 0.3

def choose_target():
    candidates = list(STATE["dirt"])
    if not candidates:
        return None, [], 0, None
    algo = STATE["algorithm"]
    memory = memory_rows()
    best = None
    best_score = float("inf")
    best_path, total_expanded, best_probability = [], 0, 0
    for target in candidates:
        path, expanded = SEARCH[algo](tuple(STATE["robot"]), target)
        total_expanded += expanded
        if not path:
            continue
        info = memory.get(target, {})
        probability = info.get("dirt_probability", 0.15)
        # A learned high-probability area gets a modest priority bonus.
        score = (len(path)-1) + (1.0 - probability) * 1.8
        if score < best_score:
            best_score, best, best_path, best_probability = score, target, path, probability
    return best, best_path, total_expanded, best_probability

def build_environment():
    dirt = set(BASE_DIRT)
    mem = memory_rows()
    # If an area has repeatedly been observed dirty, it has a chance to reappear.
    for pos, info in mem.items():
        if pos not in OBSTACLES and pos not in dirt and info["visits"] >= 2:
            if random.random() < min(0.8, info["dirt_probability"] * 0.75):
                dirt.add(pos)
    return dirt

def public_state():
    mem = memory_rows()
    facts = []
    for pos, info in sorted(mem.items(), key=lambda kv: kv[1]["dirt_probability"], reverse=True):
        if info["visits"]:
            facts.append({"location": list(pos), "visits": info["visits"],
                          "dirty_observations": info["dirty_observations"],
                          "probability": round(info["dirt_probability"], 2)})
    return {
        "robot": list(STATE["robot"]), "dock": list(DOCK),
        "width": WIDTH, "height": HEIGHT,
        "obstacles": [list(p) for p in sorted(OBSTACLES)],
        "dirt": [list(p) for p in sorted(STATE["dirt"])],
        "battery": round(STATE["battery"], 1),
        "cleaned": STATE["cleaned"], "total_dirt": STATE["total_dirt"],
        "steps": STATE["steps"], "energy_used": round(STATE["energy_used"], 1),
        "running": STATE["running"], "returning": STATE["returning"],
        "status": STATE["status"], "algorithm": STATE["algorithm"],
        "sessions": get_session_count(), "learning_score": min(99, get_session_count()*8 + len(facts)*2),
        "facts": facts[:8], "last_decision": STATE.get("last_decision", "Awaiting command"),
        "last_path": [list(p) for p in STATE.get("last_path", [])],
        "expanded": STATE.get("expanded", 0),
        "cleaning_intensity": STATE.get("cleaning_intensity", 0.0)
    }

def start_new_session(algorithm="ASTAR"):
    algorithm = algorithm.upper()
    if algorithm not in SEARCH:
        algorithm = "ASTAR"
    dirt = build_environment()
    sid = new_session_record(algorithm)
    STATE.clear()
    STATE.update({
        "session_id": sid, "robot": DOCK, "battery": 100.0, "cleaned": 0,
        "total_dirt": len(dirt), "dirt": dirt, "steps": 0, "energy_used": 0.0,
        "running": False, "returning": False, "status": "READY",
        "algorithm": algorithm, "last_decision": "Environment mapped. Agent ready.",
        "last_path": [], "expanded": 0, "cleaning_intensity": 0.0,
        "target": None
    })

def tick():
    if not STATE:
        start_new_session()
    if STATE["status"] in ("COMPLETED", "OUT_OF_ENERGY"):
        return public_state()
    if STATE["battery"] <= 1 and not STATE["returning"]:
        STATE["returning"] = True
        STATE["last_decision"] = "Expert rule fired: battery critical; return to charging dock."
    if STATE["returning"]:
        if STATE["robot"] == DOCK:
            STATE["battery"] = 100.0
            STATE["returning"] = False
            STATE["last_decision"] = "Dock reached. Battery recharged to 100%; resuming mission."
        else:
            path, expanded = astar(STATE["robot"], DOCK)
            STATE["expanded"] = expanded
            if len(path) > 1:
                STATE["robot"] = path[1]
                STATE["steps"] += 1
                STATE["battery"] = max(0, STATE["battery"] - 1.0)
                STATE["energy_used"] += 1.0
                STATE["last_path"] = path
            else:
                STATE["status"] = "OUT_OF_ENERGY"
                STATE["last_decision"] = "No safe path to dock. Mission stopped."
    else:
        target, path, expanded, probability = choose_target()
        if target is None:
            STATE["status"] = "COMPLETED"
            STATE["running"] = False
            finish_session()
            STATE["last_decision"] = "All detected dirt cleaned. Session saved to knowledge base."
            return public_state()
        STATE["target"] = target
        STATE["last_path"] = path
        STATE["expanded"] = expanded
        STATE["last_decision"] = (
            f"{STATE['algorithm']} selected {target}; learned dirt probability "
            f"{probability:.0%}; expanded {expanded} nodes."
        )
        if len(path) > 1:
            STATE["robot"] = path[1]
            STATE["steps"] += 1
            dirt_level = 0.85 if target in STATE["dirt"] else 0.2
            intensity = fuzzy_cleaning_intensity(dirt_level, STATE["battery"])
            STATE["cleaning_intensity"] = intensity
            energy = 0.55 + intensity * 0.55
            STATE["battery"] = max(0, STATE["battery"] - energy)
            STATE["energy_used"] += energy
        if STATE["robot"] in STATE["dirt"]:
            pos = STATE["robot"]
            STATE["dirt"].remove(pos)
            STATE["cleaned"] += 1
            save_observation(pos, True)
            STATE["last_decision"] = f"Tile {pos} cleaned. Knowledge base updated; fuzzy intensity {STATE['cleaning_intensity']:.2f}."
        elif STATE["robot"] != DOCK:
            save_observation(STATE["robot"], False)
        if not STATE["dirt"]:
            STATE["status"] = "COMPLETED"
            STATE["running"] = False
            finish_session()
            STATE["last_decision"] = "All detected dirt cleaned. Session saved to knowledge base."
    return public_state()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/state")
def api_state():
    if not STATE:
        start_new_session()
    return jsonify(public_state())

@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm", "ASTAR")
    if not STATE or STATE.get("status") in ("COMPLETED", "OUT_OF_ENERGY"):
        start_new_session(algorithm)
    else:
        STATE["algorithm"] = algorithm.upper() if algorithm.upper() in SEARCH else "ASTAR"
        STATE["running"] = True
        STATE["status"] = "RUNNING"
        STATE["last_decision"] = f"Agent started with {STATE['algorithm']} search."
    return jsonify(public_state())

@app.route("/api/tick", methods=["POST"])
def api_tick():
    if not STATE:
        start_new_session()
    STATE["running"] = True
    STATE["status"] = "RUNNING"
    return jsonify(tick())

@app.route("/api/pause", methods=["POST"])
def api_pause():
    if STATE:
        STATE["running"] = False
        if STATE["status"] == "RUNNING":
            STATE["status"] = "PAUSED"
        STATE["last_decision"] = "Operator paused the simulation."
    return jsonify(public_state())

@app.route("/api/new-session", methods=["POST"])
def api_new_session():
    data = request.get_json(silent=True) or {}
    start_new_session(data.get("algorithm", "ASTAR"))
    return jsonify(public_state())

@app.route("/api/algorithm", methods=["POST"])
def api_algorithm():
    data = request.get_json(silent=True) or {}
    algo = data.get("algorithm", "ASTAR").upper()
    if algo not in SEARCH:
        return jsonify({"error": "Algorithm must be BFS, DFS, or ASTAR"}), 400
    STATE["algorithm"] = algo
    STATE["last_decision"] = f"Navigation strategy changed to {algo}."
    return jsonify(public_state())

@app.route("/api/reset-memory", methods=["POST"])
def api_reset_memory():
    with db() as con:
        con.execute("UPDATE location_memory SET dirty_observations=0, visits=0, dirt_probability=0.15")
        con.execute("DELETE FROM sessions")
    start_new_session(STATE.get("algorithm", "ASTAR") if STATE else "ASTAR")
    return jsonify(public_state())

@app.route("/api/history")
def api_history():
    with db() as con:
        rows = con.execute("SELECT * FROM sessions ORDER BY id DESC LIMIT 12").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "engine": "Python Flask AI Engine", "database": "SQLite"})

if __name__ == "__main__":
    start_new_session()
    app.run(host="127.0.0.1", port=5000, debug=True)
