
from intelligence.battery import BatteryManager

# Create battery system
battery = BatteryManager()

print("Initial battery:")
battery.display_battery()

# Robot moves 10 times
for i in range(10):

    battery.movement_cost()

print("\nAfter movement:")
battery.display_battery()

# Robot cleans dirt
battery.cleaning_cost(10)

print("\nAfter cleaning:")
battery.display_battery()

# Check whether robot should return
if battery.should_return():

    print("\nRobot returning to charging station!")

else:

    print("\nRobot can continue cleaning.")

# Recharge battery
battery.recharge()

print("\nAfter recharging:")
battery.display_battery()
# Simulate battery becoming low
battery.battery = 20

print("\nTesting low battery:")

battery.display_battery()

if battery.should_return():
    print("Robot returning to charging station!")


print("\n--- Battery-Aware Navigation Test ---")

battery = BatteryManager()
battery.battery = 30

path_to_target = [(0, 0), (0, 1), (0, 2)]
path_to_charger = [(0, 2), (0, 1), (0, 0)]

result = battery.can_complete_trip(
    path_to_target,
    path_to_charger,
    dirt_amount=3
)

print("Current Battery:", battery.get_battery())
print("Can complete cleaning trip?", result)
