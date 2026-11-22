"""
from intelligence.battery import BatteryManager
from navigation.astar import astar

# Create the environment
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# Define robot, target and charging station
robot_position = (4, 4)
target = (2, 4)
charging_station = (0, 0)

# Create battery manager
battery = BatteryManager()

# Simulate a low battery
battery.battery = 20

# Find paths using A*
path_to_target = astar(grid, robot_position, target)
path_to_charger = astar(grid, target, charging_station)

print("Current Battery:", battery.get_battery())

if path_to_target and path_to_charger:

    can_clean = battery.can_complete_trip(
        path_to_target,
        path_to_charger,
        dirt_amount=3
    )

    if can_clean:
        print("Battery is sufficient.")
        print("Robot can proceed to clean.")
        print("Path to target:", path_to_target)

    else:
        print("Battery is insufficient!")
        print("Robot must return to charging station.")

        return_path = astar(
            grid,
            robot_position,
            charging_station
        )

        print("Return path:", return_path)

else:
    print("No valid path available.")
"""
#selecting a star algo 
"""
from intelligence.battery import BatteryManager
from intelligence.adaptive_strategy import AdaptiveStrategy

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

strategy = AdaptiveStrategy(5, 5)
battery = BatteryManager()

robot_position = (4, 4)
target = (2, 4)
charging_station = (0, 0)

battery.battery = 20

# Select an algorithm
exploring = False
shortest_path = True

algorithm = strategy.choose_algorithm(
    exploring=exploring,
    shortest_path=shortest_path
)

print("Selected Algorithm:", algorithm.__name__)

# Find paths using the selected algorithm
path_to_target = strategy.find_path(
    grid, robot_position, target,
    exploring, shortest_path
)

path_to_charger = strategy.find_path(
    grid, target, charging_station,
    exploring, shortest_path
)

print("Current Battery:", battery.get_battery())

if path_to_target and path_to_charger:

    can_clean = battery.can_complete_trip(
        path_to_target,
        path_to_charger,
        dirt_amount=3
    )

    if can_clean:
        print("Battery sufficient. Robot can clean.")
        print("Path to target:", path_to_target)

    else:
        print("Battery insufficient!")
        print("Robot must return to charging station.")

        return_path = strategy.find_path(
            grid, robot_position, charging_station,
            exploring, shortest_path
        )

        print("Return path:", return_path)

else:
    print("No valid path available.")
"""
#selecting DFS
"""
from intelligence.battery import BatteryManager
from intelligence.adaptive_strategy import AdaptiveStrategy

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

strategy = AdaptiveStrategy(5, 5)
battery = BatteryManager()

robot_position = (4, 4)
target = (2, 4)
charging_station = (0, 0)

battery.battery = 20

# Select an algorithm
exploring = True
shortest_path=False


algorithm = strategy.choose_algorithm(
    exploring=exploring,
    shortest_path=shortest_path
)

print("Selected Algorithm:", algorithm.__name__)

# Find paths using the selected algorithm
path_to_target = strategy.find_path(
    grid, robot_position, target,
    exploring, shortest_path
)

path_to_charger = strategy.find_path(
    grid, target, charging_station,
    exploring, shortest_path
)

print("Current Battery:", battery.get_battery())

if path_to_target and path_to_charger:

    can_clean = battery.can_complete_trip(
        path_to_target,
        path_to_charger,
        dirt_amount=3
    )

    if can_clean:
        print("Battery sufficient. Robot can clean.")
        print("Path to target:", path_to_target)

    else:
        print("Battery insufficient!")
        print("Robot must return to charging station.")

        return_path = strategy.find_path(
            grid, robot_position, charging_station,
            exploring, shortest_path
        )

        print("Return path:", return_path)

else:
    print("No valid path available.")
"""
#selecting BFS
"""
from intelligence.battery import BatteryManager
from intelligence.adaptive_strategy import AdaptiveStrategy

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

strategy = AdaptiveStrategy(5, 5)
battery = BatteryManager()

robot_position = (4, 4)
target = (2, 4)
charging_station = (0, 0)

battery.battery = 20

# Select an algorithm
exploring = False
shortest_path = False

algorithm = strategy.choose_algorithm(
    exploring=exploring,
    shortest_path=shortest_path
)

print("Selected Algorithm:", algorithm.__name__)

# Find paths using the selected algorithm
path_to_target = strategy.find_path(
    grid, robot_position, target,
    exploring, shortest_path
)

path_to_charger = strategy.find_path(
    grid, target, charging_station,
    exploring, shortest_path
)

print("Current Battery:", battery.get_battery())

if path_to_target and path_to_charger:

    can_clean = battery.can_complete_trip(
        path_to_target,
        path_to_charger,
        dirt_amount=3
    )

    if can_clean:
        print("Battery sufficient. Robot can clean.")
        print("Path to target:", path_to_target)

    else:
        print("Battery insufficient!")
        print("Robot must return to charging station.")

        return_path = strategy.find_path(
            grid, robot_position, charging_station,
            exploring, shortest_path
        )

        print("Return path:", return_path)

else:
    print("No valid path available.")
"""
"""
from intelligence.battery import BatteryManager
from intelligence.adaptive_strategy import AdaptiveStrategy

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

strategy = AdaptiveStrategy(5, 5)
battery = BatteryManager()

robot_position = (4, 4)
target = (2, 4)
charging_station = (0, 0)

battery.battery = 20

exploring = False
shortest_path = True

algorithm = strategy.choose_algorithm(
    exploring=exploring,
    shortest_path=shortest_path
)

print("Selected Algorithm:", algorithm.__name__)
print("Current Battery:", battery.get_battery())

# Find path to cleaning target
path_to_target = strategy.find_path(
    grid, robot_position, target,
    exploring, shortest_path
)

# Find path from target to charging station
path_to_charger = strategy.find_path(
    grid, target, charging_station,
    exploring, shortest_path
)

if path_to_target and path_to_charger:

    can_clean = battery.can_complete_trip(
        path_to_target,
        path_to_charger,
        dirt_amount=3
    )

    if can_clean:
        print("\nBattery sufficient. Robot can clean.")

    else:
        print("\nBattery insufficient!")
        print("Returning to charging station...")

        return_path = strategy.find_path(
            grid, robot_position, charging_station,
            exploring, shortest_path
        )

        print("Return path:", return_path)

        # Simulate movement back to charger
        for step in return_path[1:]:
            battery.movement_cost()
            robot_position = step

        print("Robot reached charging station.")
        print("Battery before charging:", battery.get_battery())

        # Recharge battery
        battery.recharge()

        print("Battery after charging:", battery.get_battery(), "%")
        print("Robot is ready to continue cleaning.")

else:
    print("No valid path available.")
"""

from intelligence.battery import BatteryManager
from intelligence.adaptive_strategy import AdaptiveStrategy

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

strategy = AdaptiveStrategy(5, 5)
battery = BatteryManager()
battery.battery = 20  # Temporarily lower battery for testing

robot_position = (4, 4)
target = (2, 4)
charging_station = (0, 0)

battery.battery = 20
dirt_amount = 3

# Choose navigation algorithm
exploring = False
shortest_path = True

algorithm = strategy.choose_algorithm(
    exploring=exploring,
    shortest_path=shortest_path
)

print("Selected Algorithm:", algorithm.__name__)
print("Current Battery:", battery.get_battery())

# Check the original cleaning trip
path_to_target = strategy.find_path(
    grid, robot_position, target,
    exploring, shortest_path
)

path_to_charger = strategy.find_path(
    grid, target, charging_station,
    exploring, shortest_path
)

if not path_to_target or not path_to_charger:
    print("No valid cleaning route available.")

else:
    can_clean = battery.can_complete_trip(
        path_to_target,
        path_to_charger,
        dirt_amount
    )

    if not can_clean:
        print("\nBattery insufficient!")
        print("Returning to charging station...")

        return_path = strategy.find_path(
            grid, robot_position, charging_station,
            exploring, shortest_path
        )

        print("Return path:", return_path)

        for step in return_path[1:]:
            battery.movement_cost()
            robot_position = step

        print("Robot reached charging station.")
        print("Battery before charging:", battery.get_battery())

        battery.recharge()

        print("Battery after charging:", battery.get_battery(), "%")

    # Resume cleaning from the charging station
    print("\nResuming cleaning task...")

    path_to_target = strategy.find_path(
        grid, robot_position, target,
        exploring, shortest_path
    )

    path_to_charger = strategy.find_path(
        grid, target, charging_station,
        exploring, shortest_path
    )

    if path_to_target and path_to_charger:

        can_clean = battery.can_complete_trip(
            path_to_target,
            path_to_charger,
            dirt_amount
        )

        if can_clean:
            print("New path to target:", path_to_target)

            for step in path_to_target[1:]:
                battery.movement_cost()
                robot_position = step

            print("Robot reached cleaning target:", robot_position)

            battery.cleaning_cost(dirt_amount)

            print("Target cleaned successfully!")
            print("Remaining Battery:", battery.get_battery(), "%")

        else:
            print("Battery insufficient even after recharging.")

    else:
        print("No valid route found after recharging.")
