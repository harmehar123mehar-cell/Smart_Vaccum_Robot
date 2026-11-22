
from collections import deque


def bfs(grid, start, goal):

    # Number of rows and columns
    rows = len(grid)
    cols = len(grid[0])

    # Queue stores cells waiting to be explored
    queue = deque([start])

    # Keep track of visited cells
    visited = {start}

    # Remember where each cell came from
    parent = {start: None}

    # Possible movements: up, down, left, right
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:

        # Take the first cell from the queue
        current = queue.popleft()

        # Check if destination is reached
        if current == goal:

            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        r, c = current

        # Explore all four neighbouring cells
        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            neighbour = (nr, nc)

            # Check boundaries, obstacles and visited cells
            if (0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0 and
                neighbour not in visited):

                visited.add(neighbour)

                parent[neighbour] = current

                queue.append(neighbour)

    return []