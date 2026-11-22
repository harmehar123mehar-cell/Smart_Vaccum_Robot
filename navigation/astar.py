
import heapq


# Calculate Manhattan Distance
def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    # Priority queue
    open_list = []

    # Initially, start node has g-cost 0
    heapq.heappush(
        open_list,
        (heuristic(start, goal), 0, start)
    )

    # Store previous positions
    parent = {start: None}

    # Cost from start to each cell
    g_cost = {start: 0}

    # Already explored cells
    visited = set()

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    while open_list:

        # Get cell with lowest f-cost
        f, current_g, current = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)

        # Check whether goal is reached
        if current == goal:

            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        r, c = current

        # Explore neighbours
        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            neighbour = (nr, nc)

            # Check grid boundaries
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            # Avoid obstacles
            if grid[nr][nc] == 1:
                continue

            # Avoid already explored cells
            if neighbour in visited:
                continue

            # Calculate new g-cost
            new_g = g_cost[current] + 1

            if new_g < g_cost.get(neighbour, float("inf")):

                g_cost[neighbour] = new_g

                parent[neighbour] = current

                # Calculate f-cost
                new_f = new_g + heuristic(neighbour, goal)

                heapq.heappush(
                    open_list,
                    (new_f, new_g, neighbour)
                )

    return []