
def dfs(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    # Stack stores cells to explore
    stack = [start]

    # Track visited cells
    visited = {start}

    # Store previous cell
    parent = {start: None}

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    while stack:

        # Take the last added cell
        current = stack.pop()

        if current == goal:

            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        r, c = current

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            neighbour = (nr, nc)

            if (0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0 and
                neighbour not in visited):

                visited.add(neighbour)

                parent[neighbour] = current

                stack.append(neighbour)

    return []