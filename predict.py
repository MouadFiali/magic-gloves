import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import joblib
import serial
import threading

new_model = load_model('rnn_model.h5')
new_model.summary()
scaler = joblib.load('rnn_scaler.joblib')
serial_4_data = ''
serial_7_data = ''

def predict_class(values):
    new_values = [float(x) for x in values.split(',')]
    
    # Reshape the array to be 2D
    new_values_reshaped = np.array(new_values).reshape(1, -1)
    
    # Scale the values
    new_values_scaled = scaler.transform(new_values_reshaped)

    # Further reshape for the model if necessary
    new_values_model_ready = new_values_scaled.reshape((1, 1, new_values_scaled.shape[1]))

    new_predictions = new_model.predict(new_values_model_ready)
    print("Classes :", new_predictions)
    predicted_class = np.argmax(new_predictions, axis=-1)
    print("Classe prédite :", predicted_class)



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

# LEFT
ser = serial.Serial('/dev/ttyACM1', 9600)

# RIGHT
ser2 = serial.Serial('/dev/ttyACM0', 9600)




            
# Create and open a CSV file for writing
count = 0
while count < 20:
    my_data = ''
    thread_serial_7 = threading.Thread(target=read_data, args=(ser,7))
    thread_serial_4 = threading.Thread(target=read_data, args=(ser2,4))
    thread_serial_4.start()
    thread_serial_7.start()
    thread_serial_4.join()
    thread_serial_7.join()
    print('thread serial 4:')
    print(str(serial_4_data))
    print('thread serial 7:')
    print(str(serial_7_data))
    if not str(serial_4_data).endswith('calibration AccGyro') and str(serial_4_data) != 'Debut de calibration Flex' and str(serial_4_data) != 'Fin de calibration' and str(serial_4_data) != 'Debut Enregistrement...' :
        my_data = format_data(serial_7_data) + ',' + format_data(serial_4_data)
        print('***********************************************************')
        predict_class(my_data)
        print('***********************************************************')

        #print('data : ')
        #print(my_data)
    elif serial_4_data.endswith('calibration AccGyro'):
        print('Calibration AccGyro en cours...')
    elif serial_4_data == 'Debut de calibration Flex':
        print('Calibration Flex en cours...')
    elif serial_4_data == 'Fin de calibration':
        print('Calibration terminee')
    elif serial_4_data == 'Debut Enregistrement...':
        print('Enregistrement en cours...')

