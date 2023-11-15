import serial

# Read the data sent by Arduino to the serial port COM4
ser = serial.Serial('COM4', 9600)  

# Create and open a CSV file for writing
while True:
    data = ser.readline().decode('utf-8').strip()
    if data:
        with open('sensor_data.csv', 'a', newline='') as csvfile:
            csvfile.write(data + '\n')
