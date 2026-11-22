
import time


class KnowledgeBase:

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        # Store dirt information
        self.dirt_map = [
            [0 for _ in range(cols)]
            for _ in range(rows)
        ]

        # Store visited cells
        self.visited_map = [
            [False for _ in range(cols)]
            for _ in range(rows)
        ]

        # Store obstacle information
        self.obstacle_map = [
            [None for _ in range(cols)]
            for _ in range(rows)
        ]

        # Store number of visits
        self.visit_count = [
            [0 for _ in range(cols)]
            for _ in range(rows)
        ]

        # Store cleaning time
        self.last_cleaned = [
            [None for _ in range(cols)]
            for _ in range(rows)
        ]

    # Update robot's knowledge
    def update_cell(self, x, y, dirt, obstacle=False):

        self.dirt_map[x][y] = dirt

        self.visited_map[x][y] = True

        self.obstacle_map[x][y] = obstacle

        self.visit_count[x][y] += 1

    # Mark a cell as cleaned
    def mark_cleaned(self, x, y):

        self.dirt_map[x][y] = 0

        self.last_cleaned[x][y] = time.time()

    # Display knowledge map
    def display_knowledge(self):

        print("\nRobot Knowledge Map:")

        for x in range(self.rows):

            row = []

            for y in range(self.cols):

                if self.obstacle_map[x][y] is True:
                    row.append("X")

                elif not self.visited_map[x][y]:
                    row.append("?")

                elif self.dirt_map[x][y] == 0:
                    row.append("C")

                else:
                    row.append("D")

            print(row)

    # Get number of visits
    def get_visits(self, x, y):

        return self.visit_count[x][y]
