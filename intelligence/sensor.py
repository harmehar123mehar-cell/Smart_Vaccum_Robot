
import random


class DirtSensor:

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        self.dirt_map = [
            [random.randint(0, 3) for _ in range(cols)]
            for _ in range(rows)
        ]

    def display_dirt(self):

        print("Current Dirt Map:")

        for row in self.dirt_map:
            print(row)

    def detect_dirt(self, x, y):

        return self.dirt_map[x][y]

    def clean_dirt(self, x, y):

        dirt_removed = self.dirt_map[x][y]

        self.dirt_map[x][y] = 0

        return dirt_removed

    def generate_new_dirt(self):

        x = random.randint(0, self.rows - 1)
        y = random.randint(0, self.cols - 1)

        self.dirt_map[x][y] = random.randint(1, 3)

        print("New dirt generated at:", (x, y))


