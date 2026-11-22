"""
class BatteryManager:

    def __init__(self):

        self.battery = 100
        self.low_battery = 25

    # Reduce battery when robot moves
    def movement_cost(self):

        self.battery -= 2

        if self.battery < 0:
            self.battery = 0

    # Reduce battery when robot cleans
    def cleaning_cost(self, dirt_amount):

        self.battery -= dirt_amount * 2

        if self.battery < 0:
            self.battery = 0

    # Check battery percentage
    def get_battery(self):

        return self.battery

    # Check whether battery is low
    def is_low(self):

        return self.battery <= self.low_battery

    # Decide whether robot should return
    def should_return(self):

        if self.is_low():
            return True

        return False

    # Recharge battery
    def recharge(self):

        self.battery = 100

    # Display battery status
    def display_battery(self):

        print("Battery:", self.battery, "%")

        if self.is_low():
            print("WARNING: Low battery!")
        else:
            print("Battery level is sufficient.")
"""
#updated version

class BatteryManager:
    def __init__(self):
        self.battery = 100
        self.low_battery = 25
        self.safety_reserve = 10

    def movement_cost(self):
        self.battery = max(0, self.battery - 2)

    def cleaning_cost(self, dirt_amount):
        self.battery = max(0, self.battery - dirt_amount * 2)

    def get_battery(self):
        return self.battery

    def is_low(self):
        return self.battery <= self.low_battery

    def estimate_movement_cost(self, path):
        if not path:
            return float("inf")

        steps = len(path) - 1
        return steps * 2

    def can_complete_trip(self, path_to_target, path_to_charger, dirt_amount):
        target_cost = self.estimate_movement_cost(path_to_target)
        return_cost = self.estimate_movement_cost(path_to_charger)
        cleaning_energy = dirt_amount * 2

        total_required = (
            target_cost
            + cleaning_energy
            + return_cost
            + self.safety_reserve
        )

        return self.battery >= total_required

    def should_return(self):
        return self.is_low()

    def recharge(self):
        self.battery = 100

    def display_battery(self):
        print("Battery:", self.battery, "%")

        if self.is_low():
            print("WARNING: Low battery! Return to charging station.")
        else:
            print("Battery level is sufficient.")
