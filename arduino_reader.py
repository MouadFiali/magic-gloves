import serial
import threading

serial_4_data = ''
serial_7_data = ''

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
        global serial_4_data
        serial_4_data = serial_port.readline().decode('utf-8').strip()
    elif port_number == 7:
        global serial_7_data
        serial_7_data = serial_port.readline().decode('utf-8').strip()
    print("Thread ended")
    
# Read the data sent by Arduino to the serial port COM
input('Appuyez sur une touche pour commencer...')
ser = serial.Serial('COM7', 9600)
ser2 = serial.Serial('COM4', 9600)


            
# Create and open a CSV file for writing
while True:
    my_data = ''
    thread_serial_7 = threading.Thread(target=read_data, args=(ser,7))
    thread_serial_4 = threading.Thread(target=read_data, args=(ser2,4))
    thread_serial_4.start()
    thread_serial_7.start()
    thread_serial_4.join()
    thread_serial_7.join()
    
    my_data = serial_7_data + serial_4_data
    if my_data and str(serial_4_data) != 'Debut de calibration' and str(serial_4_data) != 'Fin de calibration':
        with open('sensor_data.csv', 'a', newline='') as csvfile:
            csvfile.write(format_data(my_data) + '\n')
    elif serial_7_data == 'Debut de calibration':
        print('Calibration en cours...')
    elif serial_7_data == 'Fin de calibration':
        print('Calibration terminee')

# data = "225,198,131,0,223,16.00,16.00,-34.00,-2.00,-2.00,-1.00,228,196,133,0,217,16.00,16.00,-34.00,-4.00,0.00,-1.00,226,197,131,0,217,16.00,16.00,-34.00,-4.00,4.00,0.00,226,197,132,0,217,16.00,16.00,-34.00,-6.00,5.00,2.00,228,196,131,0,217,16.00,16.00,-34.00,-6.00,5.00,3.00,228,196,132,0,217,16.00,16.00,-34.00,-6.00,0.00,1.00,225,197,130,0,217,16.00,16.00,-34.00,-8.00,3.00,3.00,228,196,131,0,223,16.00,16.00,-34.00,-6.00,6.00,3.00,226,196,131,0,217,16.00,16.00,-34.00,-6.00,2.00,2.00,229,197,132,0,223,16.00,16.00,-34.00,-6.00,2.00,2.00,226,197,130,0,223,16.00,16.00,-34.00,-6.00,4.00,2.00,228,197,131,0,223,16.00,16.00,-34.00,-6.00,5.00,2.00,226,198,132,0,217,16.00,16.00,-34.00,-6.00,4.00,2.00,226,197,131,0,217,16.00,16.00,-34.00,-7.00,11.00,7.00,226,197,131,0,223,16.00,16.00,-34.00,-18.00,14.00,23.00,228,197,130,0,223,16.00,16.00,-34.00,-24.00,43.00,3.00,225,196,130,0,223,16.00,16.00,-28.00,19.00,50.00,50.00,228,198,133,0,217,33.00,16.00,-34.00,-19.00,5.00,29.00,228,197,132,0,223,16.00,16.00,-34.00,-3.00,1.00,-16.00,229,197,133,0,223,16.00,16.00,-34.00,-5.00,5.00,-5.00,"

# print(format_data(data))