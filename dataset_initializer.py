import csv

# Define the column names for left arm
columns_left = [
    "-".join([prefix + str(i), "Frame", str(n)])
    for prefix in ["Flex-Left-"]
    for i in range(1, 6)  # For 5 flex sensors
    for n in range(1, 21)
] + [
    prefix + "-Frame-" + str(n) for n in range(1, 21) for prefix in ["Position-X-Left", "Position-Y-Left", "Position-Z-Left"]
] + [
    prefix + "-Frame-" + str(n) for n in range(1, 21) for prefix in ["Orientation-X-Left", "Orientation-Y-Left", "Orientation-Z-Left"]
]

# Define the column names for right arm
columns_right = [
    "-".join([prefix + str(i), "Frame", str(n)])
    for prefix in ["Flex-Right-"]
    for i in range(1, 6)  # For 5 flex sensors
    for n in range(1, 21)
] + [
    prefix + "-Frame-" + str(n) for n in range(1, 21) for prefix in ["Position-X-Right", "Position-Y-Right", "Position-Z-Right"]
] + [
    prefix + "-Frame-" + str(n) for n in range(1, 21) for prefix in ["Orientation-X-Right", "Orientation-Y-Right", "Orientation-Z-Right"]
]

# Combine right and right arm columns
columns = columns_right + columns_left

# Initialize the CSV file with the column names
with open("sensor_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(columns_right)
print(columns_right)