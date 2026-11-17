from .astar import astar


def select_target(grid, dirt_map, robot_position):
    rows = len(grid)
    cols = len(grid[0])

    best_target = None
    best_path = []
    best_score = -1

    for r in range(rows):
        for c in range(cols):

            dirt = dirt_map[r][c]

            if dirt <= 0:
                continue

            target = (r, c)

            path = astar(grid, robot_position, target)

            if not path:
                continue

            distance = len(path) - 1
            score = dirt / (distance + 1)

            if score > best_score:
                best_score = score
                best_target = target
                best_path = path

    return best_target, best_path