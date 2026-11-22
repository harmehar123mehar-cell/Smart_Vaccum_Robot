
class DustPrediction:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # Stores how often each cell becomes dirty
        self.dirt_frequency = [
            [0 for _ in range(cols)]
            for _ in range(rows)
        ]

        # Stores how many times each cell has been cleaned
        self.cleaning_count = [
            [0 for _ in range(cols)]
            for _ in range(rows)
        ]

    def record_cleaning(self, x, y):
        self.cleaning_count[x][y] += 1

    def record_dirt(self, x, y):
        self.dirt_frequency[x][y] += 1

    def predict_dirt(self, x, y):
        if self.cleaning_count[x][y] == 0:
            return 0

        return (
            self.dirt_frequency[x][y]
            / self.cleaning_count[x][y]
        )

    def display_predictions(self):
        print("\nPredicted Dirt Map:")

        for x in range(self.rows):
            row = []

            for y in range(self.cols):
                prediction = self.predict_dirt(x, y)
                row.append(round(prediction, 2))

            print(row)
