# 🤖 Intelligent Vacuum Cleaner System

A Python-based simulation of an intelligent autonomous vacuum cleaner that navigates a grid environment, detects dirt, avoids obstacles, selects cleaning targets, manages battery consumption, and maintains cleaning records.

## 📌 Project Overview

The Intelligent Vacuum Cleaner System demonstrates how artificial intelligence concepts and search algorithms can be applied to an autonomous cleaning robot.

The robot operates in a **5×5 grid environment** containing dirty cells, clean cells, and obstacles. It uses navigation algorithms to find paths and intelligent modules to make cleaning decisions.

The project is developed using Python and follows a modular programming approach.

## ✨ Features

### 1. Navigation Algorithms
The system incorporates three pathfinding algorithms:

- **A* Search:** Uses a heuristic to find an efficient path to the target.
- **Breadth-First Search (BFS):** Explores the grid level by level and finds a shortest path in an unweighted environment.
- **Depth-First Search (DFS):** Explores one path deeply before backtracking.

Users can select the navigation algorithm through terminal input.

### 2. Dirt Sensor
- Generates a random dirt map.
- Detects dirt levels at individual grid locations.
- Cleans dirt from selected cells.
- Supports generation of new dirt.

### 3. Knowledge Base
- Stores known dirt levels.
- Maintains visited and obstacle maps.
- Tracks cell visit counts.
- Records the last-cleaned timestamps.

### 4. Battery Management
- Starts with 100% battery.
- Calculates energy consumption during movement and cleaning.
- Checks whether the robot has enough energy to complete a cleaning trip.
- Includes a 10% safety reserve.
- Supports automatic return to the charging station and recharging.

### 5. Cleaning History
- Records cleaned coordinates.
- Stores the amount of dirt removed and cleaning time.
- Calculates the total amount of dirt cleaned.

### 6. Dust Prediction
- Tracks how frequently dirt is detected at different locations.
- Maintains cleaning counts.
- Calculates a basic dirt recurrence indicator to identify locations where dirt may repeatedly occur.

### 7. Adaptive Strategy
- Selects the next cleaning target based on dirt level, visited status, and prediction score.
- Avoids obstacle locations.
- Integrates with A*, BFS, and DFS to generate navigation paths.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub
- **Concepts:** Artificial Intelligence, Search Algorithms, Pathfinding, Decision-Making, Grid-Based Simulation, Modular Programming

## 📁 Project Structure

```text
Vacuum_Cleaner_Project/
│
├── navigation/
│   ├── __init__.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── astar.py
│   └── target_selection.py
│
├── intelligence/
│   ├── __init__.py
│   ├── sensor.py
│   ├── test_sensor.py
│   ├── knowledge_base.py
│   ├── test_kb.py
│   ├── battery.py
│   ├── test_battery.py
│   ├── cleaning_history.py
│   ├── test_history.py
│   ├── dust_prediction.py
│   ├── test_prediction.py
│   ├── adaptive_strategy.py
│   └── test_integration.py
│
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### Prerequisites
- Python 3 installed on your computer.
- Git installed on your computer.
- Visual Studio Code (recommended).

### Steps

**1. Clone the repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**2. Navigate to the project directory**

```bash
cd Intelligent-Vacuum-Cleaner
```

**3. Run the integrated simulation**

```bash
python -m intelligence.test_integration
```

**4. Select a navigation algorithm**

When prompted in the terminal, enter:

- `1` for A*
- `2` for BFS
- `3` for DFS

The simulation will then execute the cleaning process.

## ▶️ How the System Works

1. The system creates a 5×5 grid environment.
2. Dirt is randomly generated across the grid.
3. Obstacles are defined in the environment.
4. The knowledge base is updated with environmental information.
5. The user selects a navigation algorithm.
6. The adaptive strategy selects a suitable dirty cell.
7. The robot calculates a path to the target and back to the charging station.
8. The battery manager checks whether sufficient energy is available.
9. The robot cleans the selected cell or recharges when necessary.
10. The system updates the knowledge base, cleaning history, battery, and dust prediction.
11. The process repeats until all known dirty cells have been cleaned.

## 🧪 Testing

Individual modules have separate test files to verify their functionality.

Examples:

```bash
python -m intelligence.test_sensor
python -m intelligence.test_kb
python -m intelligence.test_battery
python -m intelligence.test_history
python -m intelligence.test_prediction
python -m intelligence.test_strategy
```

The integrated simulation can be tested using:

```bash
python -m intelligence.test_integration
```

## ⚠️ Current Limitations

- The environment is currently limited to a 5×5 grid.
- Initial dirt distribution is random.
- Dust prediction uses a basic statistical recurrence calculation, not machine learning.
- Algorithm selection is user-controlled.
- New dirt is not continuously generated during the main integration loop.
- The project is a software simulation and does not control physical robot hardware.

## 🚀 Future Enhancements

- Develop a graphical user interface.
- Support larger and dynamically changing environments.
- Add continuous dirt generation and real-time updates.
- Improve prediction using machine-learning techniques.
- Integrate real sensors and hardware.
- Add visual representation of the robot's movement and cleaning process.

## 🎯 Project Outcome

The project demonstrates how navigation algorithms, environmental knowledge, decision-making, battery management, and cleaning records can be integrated to simulate an intelligent autonomous vacuum cleaner.

It provides a practical demonstration of AI search techniques and modular software development.

## 👥 Contributors

Harmehar Kaur Suri , Disha Pokhariyal , Bhavika Jain

---

**Project:** Intelligent Vacuum Cleaner System  
**Language:** Python  
**Academic Year:** 2026–2027