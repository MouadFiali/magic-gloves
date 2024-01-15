import queue
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import joblib
import openai
from dotenv import load_dotenv
import os

load_dotenv()

class Prediction:
    def __init__(self):
        self.new_model = load_model('rnn_model.h5')
        self.new_model.summary()
        self.scaler = joblib.load('rnn_scaler.joblib')
        self.right_serial_data = ''
        self.left_serial_data = ''
        self.serial_right_name = ''
        self.serial_left_name = ''
        self.words_dict = {0: 'PAUSE', 1: 'PROUD', 2: 'STUDENT', 3: 'THANK YOU', 4: 'THIS', 5: 'WE', 6: 'WORK'}
        # Create a queue and a thread for the GPT API
        self.q = queue.Queue()
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def predict_class(self, values):
        new_values = [float(x) for x in values.split(',')]
        
        # Reshape the array to be 2D
        new_values_reshaped = np.array(new_values).reshape(1, -1)
        
        # Scale the values
        new_values_scaled = self.scaler.transform(new_values_reshaped)

        # Further reshape for the model if necessary
        new_values_model_ready = new_values_scaled.reshape((1, 1, new_values_scaled.shape[1]))

        new_predictions = self.new_model.predict(new_values_model_ready)
        print("Classes :", new_predictions)
        predicted_class = np.argmax(new_predictions, axis=-1)
        print("Classe prédite :", predicted_class)
        print("Mot :", self.words_dict[predicted_class[0]])
        return self.words_dict[predicted_class[0]]

    # This is the function that will run in the thread to send the data to the GPT API
    def thread_func(self):
        while True:
            args = self.q.get()
            if args is None:
                break
            self.words_to_sentence(*args)
    
    def set_serial_ports(self, port_name, port_number):
        if port_number == 1:
            self.serial_right_name = port_name
        elif port_number == 0:
            print("Left port connected: " + port_name)
            self.serial_left_name = port_name

    def words_to_sentence(self, words, qThread):
        # time.sleep(2)
        list_word = ' - '.join(words)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in the NLP field and creating meaningful sentences from words is your specialty."},
                {"role": "user", "content": "Transform the given sequences of words into complete sentences according to the following pattern: Replace ',' with appropriate connecting words, Maintain the order of the words as given, Expand abbreviations and correct any typos to form coherent sentences. Given words: " + list_word}
            ]
        )
        qThread.result_signal.emit(response['choices'][0].message.content)
        # qThread.result_signal.emit(list_word)
    
    def read_data(self, serial_port, port_number):
        print("Thread started")
        if port_number == 1:
            self.right_serial_data = serial_port.readline().decode('utf-8').strip()
        elif port_number == 0:
            self.left_serial_data = serial_port.readline().decode('utf-8').strip()
        print("Thread ended")

    def format_data(self, data):
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
    
    def format_all_data(self):
        return self.format_data(self.left_serial_data) + ',' + self.format_data(self.right_serial_data)




