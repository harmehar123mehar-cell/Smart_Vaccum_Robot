"""
from intelligence.adaptive_strategy import AdaptiveStrategy

strategy = AdaptiveStrategy(3, 3)

dirt_map = [
    [1, 0, 2],
    [0, 3, 1],
    [2, 0, 0]
]

visited_map = [
    [True, False, True],
    [False, False, True],
    [True, False, False]
]

predictions = [
    [1, 0, 2],
    [0, 1, 0],
    [3, 0, 0]
]

next_cell = strategy.choose_next_cell(
    dirt_map,
    visited_map,
    predictions
)

print("Next cell selected for cleaning:", next_cell)
"""

from intelligence.adaptive_strategy import AdaptiveStrategy

strategy = AdaptiveStrategy(3, 3)

dirt_map = [
    [1, 0, 2],
    [0, 3, 1],
    [2, 0, 0]
]

visited_map = [
    [True, False, True],
    [False, False, True],
    [True, False, False]
]

predictions = [
    [1, 0, 2],
    [0, 1, 0],
    [3, 0, 0]
]

grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

robot_position = (0, 0)

target = strategy.choose_next_cell(
    dirt_map,
    visited_map,
    predictions
)

print("Selected cleaning target:", target)

path = strategy.find_path(
    grid,
    robot_position,
    target
)

print("Path selected using A*:", path)

path_dfs = strategy.find_path(
    grid,
    robot_position,
    target,
    exploring=True
)

print("Path selected using DFS:", path_dfs)

path_bfs = strategy.choose_algorithm(
    exploring=False,
    shortest_path=False
)(grid, robot_position, target)

print("Path selected using BFS:", path_bfs)
