"""#initial
class AdaptiveStrategy:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def choose_next_cell(self, dirt_map, visited_map, predictions):
        best_cell = None
        highest_score = -1

        for x in range(self.rows):
            for y in range(self.cols):

                # Skip cells that are already clean
                if dirt_map[x][y] == 0:
                    continue

                # Dirt amount contributes most to the score
                score = dirt_map[x][y] * 2

                # Give priority to cells that have not been visited
                if not visited_map[x][y]:
                    score += 3

                # Add predicted future dirt
                score += predictions[x][y]

                if score > highest_score:
                    highest_score = score
                    best_cell = (x, y)

        return best_cell
"""

from navigation.bfs import bfs
from navigation.dfs import dfs
from navigation.astar import astar


class AdaptiveStrategy:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
    """
    def choose_next_cell(self, dirt_map, visited_map, predictions):
        best_cell = None
        highest_score = -1

        for x in range(self.rows):
            for y in range(self.cols):

                if dirt_map[x][y] <= 0:
                    continue

                score = dirt_map[x][y] * 2

                if not visited_map[x][y]:
                    score += 3

                score += predictions[x][y]

                if score > highest_score:
                    highest_score = score
                    best_cell = (x, y)

        return best_cell
    """

    def choose_next_cell(self, dirt_map, visited_map, predictions, grid=None):
        best_cell = None
        highest_score = -1

        for x in range(self.rows):
            for y in range(self.cols):

                # Skip cells without dirt
                if dirt_map[x][y] <= 0:
                    continue

                # Skip obstacles
                if grid is not None and grid[x][y] == 1:
                    continue

                score = dirt_map[x][y] * 2

                if not visited_map[x][y]:
                    score += 3

                score += predictions[x][y]

                if score > highest_score:
                    highest_score = score
                    best_cell = (x, y)

        return best_cell
    """
    def choose_algorithm(self, exploring=False, shortest_path=True):
        if exploring:
            return dfs

        if shortest_path:
            return astar

        return bfs

    def find_path(self, grid, start, goal, exploring=False):
        algorithm = self.choose_algorithm(
            exploring=exploring,
            shortest_path=True
        )

        return algorithm(grid, start, goal)
    """
    
    def choose_algorithm(self, exploring=False, shortest_path=True):
        if exploring:
            return dfs
        elif shortest_path:
            return astar
        else:
            return bfs


    def find_path(self, grid, start, goal,
                exploring=False, shortest_path=True):

        algorithm = self.choose_algorithm(
            exploring=exploring,
            shortest_path=shortest_path
        )

        return algorithm(grid, start, goal)
