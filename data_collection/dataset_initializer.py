import csv

# Define the column names for left arm
columns_left = [
    "-".join([prefix + str(i), "Frame", str(n)])
    for prefix in ["Flex-Left-"]
    for i in range(1, 6)  # For 5 flex sensors
    for n in range(1, 21)
] + [
    prefix + "-Frame-" + str(n) for n in range(1, 21) for prefix in ["Acceleration-X-Left", "Acceleration-Y-Left", "Acceleration-Z-Left"]
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
    prefix + "-Frame-" + str(n) for n in range(1, 21) for prefix in ["Acceleration-X-Right", "Acceleration-Y-Right", "Acceleration-Z-Right"]
] + [
    prefix + "-Frame-" + str(n) for n in range(1, 21) for prefix in ["Orientation-X-Right", "Orientation-Y-Right", "Orientation-Z-Right"]
]

# Combine right and right arm columns
columns = columns_left + columns_right

# Initialize the CSV file with the column names
with open("sensor_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # Add the SIGN column
    writer.writerow(columns + ["SIGN"])
print("CSV file initialized")