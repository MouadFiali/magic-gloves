import serial

ser = serial.Serial('COM4', 9600)  

# Create and open a CSV file for writing
with open('sensor_data.csv', 'w', newline='') as csvfile:
    with open('sensor_data.csv', 'a', newline='') as csvfile:
        csvfile.write("AccelX, AccelY, AccelZ, Flex1, Flex2, Flex3, Flex4, Flex5\n")
    while True:
        data = ser.readline().decode('utf-8').strip()
        if data:
            with open('sensor_data.csv', 'a', newline='') as csvfile:
                csvfile.write(data + '\n')
