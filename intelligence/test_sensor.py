
from intelligence.sensor import DirtSensor

sensor = DirtSensor(5, 5)

print("\n--- INITIAL DIRT MAP ---")
sensor.display_dirt()

robot_position = (2, 3)

# Detect dirt
dirt = sensor.detect_dirt(*robot_position)

print("\nDirt detected at", robot_position, ":", dirt)

# Clean dirt
removed = sensor.clean_dirt(*robot_position)

print("\nDirt removed:", removed)

# Display updated map
print("\n--- UPDATED DIRT MAP ---")
sensor.display_dirt()

# Generate new dirt  remove it from here once done with the project 
sensor.generate_new_dirt()

print("\n--- FINAL DIRT MAP ---")
sensor.display_dirt()
