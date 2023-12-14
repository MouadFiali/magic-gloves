import serial
import threading

serial_right_data = ''
serial_left_data = ''

# Function to format the data sent by Arduino in order to fit the columns structure of the CSV file
def format_data(data):
    data = data[:-1]
    data = data.split(',')
    flex_data = [[] for i in range(5)]
    position_data = []
    orientation_data = []
    i = 0
    print(len(data))
    while(i < len(data)):
        for j in range(5):
            flex_data[j].append(data[i+j])
        i = i + 5

        for j in range(3):
            position_data.append(data[i+j])
        i = i + 3

        for j in range(3):
            orientation_data.append(data[i+j])
        i = i + 3

    # Add the data in one string to write in the CSV file
    line = ''
    for i in range(5):
        for j in range(len(flex_data[i])):
            line += flex_data[i][j] + ','
    for i in range(len(position_data)):
        line += position_data[i] + ','
    for i in range(len(orientation_data)):
        line += orientation_data[i] + ','        

    return line[:-1]

def read_data(serial_port, port_number):
    print("Thread started")
    if port_number == 4:
        global serial_right_data
        serial_right_data = serial_port.readline().decode('utf-8').strip()
    elif port_number == 7:
        global serial_left_data
        serial_left_data = serial_port.readline().decode('utf-8').strip()
    print("Thread ended")
    
# Read the data sent by Arduino to the serial port COM
input('Appuyez sur une touche pour commencer...')
# LEFT
ser = serial.Serial('COM7', 9600)
# RIGHT
ser2 = serial.Serial('COM4', 9600)


# Loop to read the data sent by Arduino to the serial port COM            
count = 0
while count < 20:
    my_data = ''
    # For each hand, we create a thread to read the data so that we can read both hands at the same time
    thread_serial_left = threading.Thread(target=read_data, args=(ser,7))
    thread_serial_right = threading.Thread(target=read_data, args=(ser2,4))
    thread_serial_right.start()
    thread_serial_left.start()
    thread_serial_right.join()
    thread_serial_left.join()
    
    if str(serial_right_data) != 'Debut de calibration AccGyro' and str(serial_right_data) != 'Debut de calibration Flex' and str(serial_right_data) != 'Fin de calibration' and str(serial_right_data) != 'Debut Enregistrement...' :
        my_data = format_data(serial_left_data) + ',' + format_data(serial_right_data) + ',' + 'THANK YOU'
        with open('sensor_data.csv', 'a', newline='') as csvfile:
            csvfile.write(my_data + '\n')
            count += 1
    # When the data sent by Arduino is not the one we want to write in the CSV file, we print it in the console
    # to show the steps of what is happening in the Arduino code
    elif serial_right_data == 'Debut de calibration AccGyro':
        print('Calibration AccGyro en cours...')
    elif serial_right_data == 'Debut de calibration Flex':
        print('Calibration Flex en cours...')
    elif serial_right_data == 'Fin de calibration':
        print('Calibration terminee')
    elif serial_right_data == 'Debut Enregistrement...':
        print('Enregistrement en cours...')

