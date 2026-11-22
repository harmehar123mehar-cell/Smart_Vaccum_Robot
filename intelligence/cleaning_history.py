import time

class CleaningHistory:
    def __init__(self):
        self.history = []

    def record_cleaning(self, x, y, dirt_removed):
        record = {
            "x": x,
            "y": y,
            "dirt_removed": dirt_removed,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        self.history.append(record)

    def show_history(self):
        print("\nCleaning History:")

        if not self.history:
            print("No cleaning has been recorded yet.")
            return

        for record in self.history:
            print(record)

    def total_dirt_cleaned(self):
        total = 0

        for record in self.history:
            total += record["dirt_removed"]

        return total
