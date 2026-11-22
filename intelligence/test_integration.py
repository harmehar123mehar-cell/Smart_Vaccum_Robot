
from intelligence.sensor import DirtSensor
from intelligence.knowledge_base import KnowledgeBase
from intelligence.battery import BatteryManager
from intelligence.cleaning_history import CleaningHistory
from intelligence.dust_prediction import DustPrediction
from intelligence.adaptive_strategy import AdaptiveStrategy

# Create a 5x5 environment
rows = 5
cols = 5

sensor = DirtSensor(rows, cols)
knowledge = KnowledgeBase(rows, cols)
battery = BatteryManager()
#Temporary
#battery.battery = 10
history = CleaningHistory()
prediction = DustPrediction(rows, cols)
strategy = AdaptiveStrategy(rows, cols)

# Robot's starting position
robot_position = (0, 0)
"""
# Create an obstacle-free navigation grid
grid = [[0 for _ in range(cols)] for _ in range(rows)]
"""
#Grid with Obstacle
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

print("INITIAL DIRT MAP:")
for row in sensor.dirt_map:
    print(row)

# Update robot knowledge using sensor readings
for x in range(rows):
    for y in range(cols):
        dirt = sensor.detect_dirt(x, y)
        """
        knowledge.update_cell(x, y, dirt)
        """
        knowledge.update_cell(
            x, y, dirt,
            obstacle=(grid[x][y] == 1)
        )
# Generate a dirt prediction map
for x in range(rows):
    for y in range(cols):
        if sensor.dirt_map[x][y] > 0:
            prediction.record_dirt(x, y)
            prediction.record_cleaning(x, y)

# Select the next cleaning target
"""
target = strategy.choose_next_cell(
    knowledge.dirt_map,
    knowledge.visited_map,
    [
        [prediction.predict_dirt(x, y) for y in range(cols)]
        for x in range(rows)
    ]
)
"""
"""
target = strategy.choose_next_cell(
    knowledge.dirt_map,
    knowledge.visited_map,
    [
        [prediction.predict_dirt(x, y) for y in range(cols)]
        for x in range(rows)
    ],
    grid
)
print("\nSelected cleaning target:", target)
"""
"""
if target is not None:

    # Find a path using A*
    path = strategy.find_path(
        grid,
        robot_position,
        target
    )

    print("Navigation path:", path)

    # Simulate robot movement
    for position in path[1:]:
        battery.movement_cost()

    # Clean the selected cell
    x, y = target
    dirt_removed = sensor.clean_dirt(x, y)

    battery.cleaning_cost(dirt_removed)
    history.record_cleaning(x, y, dirt_removed)
    knowledge.mark_cleaned(x, y)

    print("\nCleaning completed!")
    print("Dirt removed:", dirt_removed)

else:
    print("\nNo dirty cells found.")
"""
"""
if target is not None:

    charging_station = (0, 0)


   # Choose the navigation algorithm
    exploring = False
    shortest_path = False

    algorithm = strategy.choose_algorithm(
        exploring=exploring,
        shortest_path=shortest_path
    )

    print("\nExploring:", exploring)
    print("Shortest Path:", shortest_path)
    print("Selected Algorithm:", algorithm.__name__)
    # Find paths to the cleaning target and charging station
    path_to_target = strategy.find_path(
        grid, robot_position, target,
        exploring, shortest_path
    )

    path_to_charger = strategy.find_path(
        grid, target, charging_station,
        exploring, shortest_path
    )

    if path_to_target and path_to_charger:

        x, y = target
        dirt_amount = sensor.detect_dirt(x, y)

        # Check whether the battery can complete the entire trip
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

            if return_path:
                for position in return_path[1:]:
                    battery.movement_cost()
                    robot_position = position

                print("Robot reached charging station.")
                print("Battery before charging:", battery.get_battery(), "%")

                battery.recharge()

                print("Battery after charging:", battery.get_battery(), "%")

            else:
                print("Unable to reach charging station.")
                can_clean = False

            # Recalculate paths after recharging
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
            else:
                can_clean = False

        # Resume cleaning if sufficient battery is available
        if can_clean:
            print("\nResuming cleaning task...")
            print("Navigation path:", path_to_target)

            for position in path_to_target[1:]:
                battery.movement_cost()
                robot_position = position

            dirt_removed = sensor.clean_dirt(x, y)

            battery.cleaning_cost(dirt_removed)
            history.record_cleaning(x, y, dirt_removed)
            knowledge.mark_cleaned(x, y)

            print("\nCleaning completed!")
            print("Robot position:", robot_position)
            print("Dirt removed:", dirt_removed)

        else:
            print("\nBattery insufficient to complete cleaning safely.")

    else:
        print("\nNo valid path available.")

else:
    print("\nNo dirty cells found.")
"""

# MULTIPLE-CELL CLEANING SIMULATION

charging_station = (0, 0)

# Choose the navigation algorithm
"""
exploring = False
shortest_path = False
"""
# Ask the user to select a navigation algorithm

print("\nChoose Navigation Algorithm:")
print("1. A*")
print("2. BFS")
print("3. DFS")

choice = input("Enter your choice (1/2/3): ")

if choice == "1":
    exploring = False
    shortest_path = True

elif choice == "2":
    exploring = False
    shortest_path = False

elif choice == "3":
    exploring = True
    shortest_path = True

else:
    print("Invalid choice! Defaulting to A*.")
    exploring = False
    shortest_path = True
    
cleaning_number = 1

while True:

    # Generate the current prediction map
    predictions = [
        [prediction.predict_dirt(x, y) for y in range(cols)]
        for x in range(rows)
    ]

    # Select the next cleaning target
    target = strategy.choose_next_cell(
        knowledge.dirt_map,
        knowledge.visited_map,
        predictions,
        grid
    )

    # Stop when no dirty cells remain
    if target is None:
        print("\nAll known dirty cells have been cleaned!")
        break

    algorithm = strategy.choose_algorithm(
        exploring=exploring,
        shortest_path=shortest_path
    )

    print("\n--------------------------------")
    print("Cleaning Task:", cleaning_number)
    print("Selected Algorithm:", algorithm.__name__)
    print("Selected Target:", target)

    # Find path to target and back to charger
    path_to_target = strategy.find_path(
        grid, robot_position, target,
        exploring, shortest_path
    )

    path_to_charger = strategy.find_path(
        grid, target, charging_station,
        exploring, shortest_path
    )

    if not path_to_target or not path_to_charger:
        print("No valid path available.")
        break

    x, y = target
    dirt_amount = sensor.detect_dirt(x, y)

    # Check battery before starting the cleaning task
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

        if not return_path:
            print("Cannot reach charging station.")
            break

        for position in return_path[1:]:
            battery.movement_cost()
            robot_position = position

        print("Reached charging station.")
        print("Battery before charging:", battery.get_battery(), "%")

        battery.recharge()

        print("Battery after charging:", battery.get_battery(), "%")

        # Recalculate the trip after charging
        path_to_target = strategy.find_path(
            grid, robot_position, target,
            exploring, shortest_path
        )

        path_to_charger = strategy.find_path(
            grid, target, charging_station,
            exploring, shortest_path
        )

        if not path_to_target or not path_to_charger:
            print("No valid path after charging.")
            break

        can_clean = battery.can_complete_trip(
            path_to_target,
            path_to_charger,
            dirt_amount
        )

        if not can_clean:
            print("Insufficient battery even after charging.")
            break

    # Move towards the target
    print("Navigation Path:", path_to_target)

    for position in path_to_target[1:]:
        battery.movement_cost()
        robot_position = position

    # Clean the target
    dirt_removed = sensor.clean_dirt(x, y)

    battery.cleaning_cost(dirt_removed)

    history.record_cleaning(x, y, dirt_removed)
    knowledge.mark_cleaned(x, y)
    prediction.record_cleaning(x, y)

    print("Robot reached:", robot_position)
    print("Dirt removed:", dirt_removed)
    print("Remaining battery:", battery.get_battery(), "%")

    cleaning_number += 1


# END OF MULTIPLE-CELL CLEANING

# Display final information
print("\nFINAL BATTERY STATUS:")
battery.display_battery()

print("\nCLEANING RECORDS:")
history.show_history()

print("\nTotal dirt cleaned:", history.total_dirt_cleaned())

print("\nUPDATED KNOWLEDGE MAP:")
knowledge.display_knowledge()
