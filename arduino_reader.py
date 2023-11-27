import serial
import csv

# Read the data sent by Arduino to the serial port COM
ser = serial.Serial('COM7', 9600) 

def format_data(data):
    data = data.split(',')
    flex_data = [[] for i in range(5)]
    position_data = []
    orientation_data = []
    i = 0
    print(len(data))
    while(i < len(data)):
        for j in range(5):
            flex_data[j].append(data[i+j])
            print(i+j)
        i = i + 5

        for j in range(3):
            position_data.append(data[i+j])
            print(i+j)
        i = i + 3

        for j in range(3):
            orientation_data.append(data[i+j])
            print(i+j)
        i = i + 3
        

    return flex_data + position_data + orientation_data
            
# Create and open a CSV file for writing
while True:
    data = ser.readline().decode('utf-8').strip()
    print(data)
    if data and data != 'Début de calibration' and data != 'Fin de calibration':
        with open('sensor_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(format_data(data))
            print(data)
    elif data == 'Début de calibration':
        print('Calibration en cours...')
    elif data == 'Fin de calibration':
        print('Calibration terminée')

# data = "194,143,111,170,189,-17.00,50.00,-25.00,26.00,25.00,4.00,192,146,113,174,189,-17.00,50.00,-25.00,43.00,31.00,-4.00,194,143,113,176,189,-17.00,50.00,-25.00,50.00,46.00,-3.00,194,145,115,178,189,-17.00,50.00,-25.00,50.00,48.00,-1.00,186,148,115,183,189,-17.00,50.00,-25.00,31.00,31.00,8.00,192,150,113,181,189,-17.00,50.00,-25.00,11.00,14.00,10.00,198,155,117,185,189,-17.00,50.00,-25.00,29.00,7.00,-7.00,204,158,120,190,189,-17.00,50.00,-25.00,50.00,-50.00,-50.00,214,162,128,194,189,-17.00,50.00,-25.00,-7.00,34.00,-9.00,212,179,141,216,196,-17.00,50.00,-25.00,25.00,12.00,16.00,214,184,154,223,189,-17.00,50.00,-25.00,18.00,26.00,4.00,225,211,184,234,189,-17.00,50.00,0.00,50.00,-1.00,-45.00,241,227,201,243,189,-17.00,50.00,0.00,4.00,13.00,-13.00,243,227,207,241,189,-17.00,50.00,0.00,19.00,14.00,24.00,243,227,205,243,196,-17.00,50.00,-25.00,-2.00,29.00,-6.00,245,224,201,243,189,-17.00,50.00,-25.00,21.00,16.00,-4.00,245,231,203,243,189,-17.00,50.00,0.00,15.00,50.00,17.00,243,226,203,241,196,-17.00,50.00,-25.00,-12.00,-14.00,-20.00,247,222,201,243,189,-17.00,50.00,-25.00,8.00,17.00,1.00"

# print(format_data(data))