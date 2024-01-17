import queue
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import joblib
import serial
import threading
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

new_model = load_model('rnn_model.h5')
new_model.summary()
scaler = joblib.load('rnn_scaler.joblib')
right_serial_data = ''
left_serial_data = ''
words_dict = {0: 'PAUSE', 1: 'PROUD', 2: 'STUDENT', 3: 'THANK YOU', 4: 'THIS', 5: 'WE', 6: 'WORK'}
# Create a queue and a thread for the GPT API
q = queue.Queue() 

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
    print("Mot :", words_dict[predicted_class[0]])
    return words_dict[predicted_class[0]]

def words_to_sentence(words, count):
    global time_start
    # sleep 2 seconds before calling the API
    time.sleep(3)
    list_word = ' - '.join(words)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in the NLP field and creating meaningful sentences from words is your specialty."},
            {"role": "user", "content": "Transform the given sequences of words into complete sentences according to the following pattern: Replace ',' with appropriate connecting words, Maintain the order of the words as given, Expand abbreviations and correct any typos to form coherent sentences. Given words: " + list_word}
        ]
    )
    if count == 0:
        time_start = time.time()
    print(words)
    print(response['choices'][0].message)
    print("Time elapsed: ", time.time() - time_start, "seconds")




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
    if port_number == 1:
        global right_serial_data
        right_serial_data = serial_port.readline().decode('utf-8').strip()
    elif port_number == 0:
        global left_serial_data
        left_serial_data = serial_port.readline().decode('utf-8').strip()
    print("Thread ended")

# This is the function that will run in the thread to send the data to the GPT API
def thread_func():
    while True:
        args = q.get()
        if args is None:
            break
        words_to_sentence(*args)
    
# Read the data sent by Arduino to the serial port COM
input('Appuyez sur une touche pour commencer...')

# LEFT HAND (Change the COM port if necessary)
ser = serial.Serial('COM4', 9600)
# RIGHT HAND (Change the COM port if necessary)
ser2 = serial.Serial('COM7', 9600)

# Thread to send the data to the GPT API
thread = threading.Thread(target=thread_func)
thread.start()

# Read the data sent by Arduino to the serial port COM and predict the class
count = 0
time_start = 0
words_predicted = []
while count < 5:
    my_data = ''
    # 0 for left, 1 for right (to know which serial port to read from)
    thread_serial_left = threading.Thread(target=read_data, args=(ser,0))
    thread_serial_right = threading.Thread(target=read_data, args=(ser2,1))
    
    # Start the threads
    thread_serial_right.start()
    thread_serial_left.start()

    # Wait for the threads to finish
    thread_serial_right.join()
    thread_serial_left.join()
    
    # If the data is not a calibration message, predict the class
    if not str(right_serial_data).endswith('calibration AccGyro') and str(right_serial_data) != 'Debut de calibration Flex' and str(right_serial_data) != 'Fin de calibration' and str(right_serial_data) != 'Debut Enregistrement...' :
    
        my_data = format_data(left_serial_data) + ',' + format_data(right_serial_data)
        print('***********************************************************')
        words_predicted.append(predict_class(my_data))
        q.put((words_predicted, count))
        print('***********************************************************')
        count += 1

    # If the data is a calibration message, print it so the user knows what is happening
    elif right_serial_data.endswith('calibration AccGyro'):
        print('Calibration AccGyro en cours...')
    elif right_serial_data == 'Debut de calibration Flex':
        print('Calibration Flex en cours...')
    elif right_serial_data == 'Fin de calibration':
        print('Calibration terminee')
    elif right_serial_data == 'Debut Enregistrement...':
        print('Enregistrement en cours...')


# Stop the thread
q.put(None)
thread.join()
print("Thread stopped")


