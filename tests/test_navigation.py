import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from navigation.bfs import bfs
from navigation.dfs import dfs
from navigation.astar import astar
from navigation.target_selection import select_target


grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

bfs_path = bfs(grid, start, goal)
dfs_path = dfs(grid, start, goal)
astar_path = astar(grid, start, goal)

print("\n--- ALGORITHM COMPARISON ---")

print("BFS:", bfs_path)
print("DFS:", dfs_path)
print("A*:", astar_path)

print("\n--- PATH LENGTHS ---")

print("BFS:", len(bfs_path) - 1)
print("DFS:", len(dfs_path) - 1)
print("A*:", len(astar_path) - 1)

dirt_map = [
    [0, 2, 0, 0, 0],
    [0, 0, 5, 0, 0],
    [0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0],
    [0, 0, 0, 0, 8]
]

robot_position = (0, 0)

target, path = select_target(
    grid,
    dirt_map,
    robot_position
)

print("\n--- INTELLIGENT TARGET SELECTION ---")
print("Selected target:", target)
print("Path to target:", path)