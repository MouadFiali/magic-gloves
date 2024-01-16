import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QPixmap
import serial
from serial.tools import list_ports
from PyQt5.QtCore import QTimer
from app.predict import Prediction

class MagicGlovesUI(QWidget):
    def __init__(self):
        self.prediction = Prediction()
        super().__init__()
        # Load the image into a QImage
        image = QImage("images/magic-gloves-icon-2.jpg")

        # Convert the QImage to a QPixmap
        pixmap = QPixmap.fromImage(image)

        # Create a QPalette
        palette = QPalette()

        # Set the QPixmap as the background of the QPalette
        palette.setBrush(QPalette.Background, QBrush(pixmap))

        # Set the QPalette as the palette of the widget
        self.setPalette(palette)
        self.setWindowTitle("Magic Gloves")
        # Add icon to the window
        self.setWindowIcon(QIcon('images/magic-gloves-icon.jpg'))
        # set the size of the window
        self.setFixedSize(600, 800)
        # set the background image of the window
        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        # Add the title of the program
        self.title_label = QLabel("Magic Gloves")
        # set the font size of the title
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Add a text area to show the user what's happening in the background
        self.info_label = QLabel("En attente de l'utilisateur...\n Veuillez connecter les gants à l'ordinateur.\n Assurez-vous de connecter le gant gauche en premier.")
        # set the font size of the info and the police and add a round border
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 20px; font-style: italic; background-color: rgba(255, 255, 255, 230); border-radius: 15px;")
        # set the alignment of the info at the bottom of the window
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Add the start button
        self.start_button = QPushButton("Start")
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.setToolTip("Start the prediction")
        self.start_button.setToolTipDuration(2000)
        self.start_button.setObjectName("QPushButton")
        # Connect the button to the start_prediction function and the show_info function
        self.start_button.clicked.connect(self.start_prediction)
        # set the font size of the start button and change color to a transparent blue
        # self.start_button.setStyleSheet("font-size: 25px; background-color: rgba(45, 95, 200, 127); border-radius: 15px; color: white; font-weight: bold; border: 2px solid black;")
        self.start_button.setStyleSheet("""
        QPushButton {
            font-size: 25px; 
            background-color: rgba(45, 95, 200, 127); 
            border-radius: 15px; 
            color: white; 
            font-weight: bold; 
            border: 2px solid black;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: white; 
            color: black;
        }
        """)
        # Set limit for the size of the button
        self.start_button.setFixedWidth(300)
        self.start_button.setFixedHeight(70)
        # self.start_button.setEnabled(False)  # Disable the start button initially
        self.layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        # Add the result label
        self.result_label = QLabel("Les résultats s'afficheront ici.")
        # set the font size of the result and the police
        self.result_label.setStyleSheet("font-size: 20px; font-style: italic; background-color: rgba(255, 255, 255, 230); border-radius: 15px;")
        # set the alignment of the result at the bottom of the window
        self.result_label.setAlignment(Qt.AlignCenter)
        # Wrap the text so it doesn't go out of the window
        self.result_label.setWordWrap(True)
        self.layout.addWidget(self.result_label)

        # Add the info label
        self.advice_label = QLabel("Make sure to wear the gloves correctly and launch the program when you are ready.")
        # set the font size of the info and the police
        self.advice_label.setStyleSheet("font-size: 15px; font-style: italic;")
        # set the alignment of the info at the bottom of the window
        self.advice_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.layout.addWidget(self.advice_label)
        self.setLayout(self.layout)

        # Begin checking for ports read the ports that are connected
        self.connect_ports = [port.device for port in list_ports.comports()]
        self.initial_ports = len(self.connect_ports)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_ports)
        self.timer.start(1000)  # Check ports every second

        # Animation timers
        self.delete_timer = QTimer()
        self.delete_timer.timeout.connect(self.delete_word)
        self.type_timer = QTimer()
        self.type_timer.timeout.connect(self.type_character)
        self.result_to_type = ""

    def check_ports(self):
        ports = list_ports.comports()
        port_names = [port.device for port in ports]
        print(port_names)

        # If a new port is connected, enable the start button
        if len(port_names) > len(self.connect_ports) and len(port_names) - self.initial_ports == 1:
            # Get the name of the new port
            new_port = [port for port in port_names if port not in self.connect_ports][0]
            print("Left port connected: " + new_port)
            self.info_label.setText("Gant gauche connecté sur le port " + new_port + ".\nVeuillez connecter le gant droit.")
            self.connect_ports = port_names
            self.prediction.set_serial_ports(new_port, 0)
        if len(port_names) > len(self.connect_ports) and len(port_names) - self.initial_ports == 2:
            # Get the name of the new port
            new_port = [port for port in port_names if port not in self.connect_ports][0]
            print("Right port connected: " + new_port)
            self.info_label.setText("Gant droit connecté sur le port " + new_port + ".\nVous pouvez lancer l'application.")
            self.connect_ports = port_names
            self.prediction.set_serial_ports(new_port, 1)
            self.start_button.setEnabled(True)
            self.timer.stop()

    def start_prediction(self):
        self.show_info("Application started...")
        self.thread = PredictionThread(self)
        self.thread.result_signal.connect(self.update_result)
        self.thread.start()

    def show_info(self, info):
        # Replace the previous info with the new one
        self.info_label.setText(info)

    def update_result(self, result):
        self.result_to_type = result
        self.delete_timer.start(80)  # Delete a word every half second

    def delete_word(self):
        text = self.result_label.text()
        words = text.rsplit(" ", 1)
        if len(words) > 1:
            self.result_label.setText(words[0])
        else:
            self.result_label.clear()
            self.delete_timer.stop()
            self.type_timer.start(25)  # Type a character every tenth of a second

    def type_character(self):
        if self.result_to_type:
            self.result_label.setText(self.result_label.text() + self.result_to_type[0])
            self.result_to_type = self.result_to_type[1:]
        else:
            self.type_timer.stop()
      

class PredictionThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        # LEFT HAND
        serial_left = serial.Serial(self.ui.prediction.serial_left_name, 9600)
        # RIGHT HAND
        serial_right = serial.Serial(self.ui.prediction.serial_right_name, 9600)
        # Read the data sent by Arduino to the serial port COM and predict the class
        count = 1
        words_predicted = []
        # Start the queue
        thread = threading.Thread(target=self.ui.prediction.thread_func)
        thread.start()
        while True:
            my_data = ''
            # 0 for left, 1 for right (to know which serial port to read from)
            thread_serial_left = threading.Thread(target=self.ui.prediction.read_data, args=(serial_left,0))
            thread_serial_right = threading.Thread(target=self.ui.prediction.read_data, args=(serial_right,1))
            
            # Start the threads
            thread_serial_right.start()
            thread_serial_left.start()

            # Wait for the threads to finish
            thread_serial_right.join()
            thread_serial_left.join()
            
            # If the data is not a calibration message, predict the class
            if not str(self.ui.prediction.right_serial_data).endswith('calibration AccGyro') and str(self.ui.prediction.right_serial_data) != 'Debut de calibration Flex' and str(self.ui.prediction.right_serial_data) != 'Fin de calibration' and str(self.ui.prediction.right_serial_data) != 'Debut Enregistrement...' :
                self.ui.show_info("Pause de 2 secondes avant de passer au mot suivant...")
                my_data = self.ui.prediction.format_all_data()
                print('***********************************************************')
                predicted_word = self.ui.prediction.predict_class(my_data)
                if predicted_word != 'PAUSE':
                    words_predicted.append(predicted_word)
                # Every 2 words, send the words to the GPT API to get a sentence
                if len(words_predicted) % 2 == 0 or predicted_word == 'PAUSE':
                # if (count % 2 != 0 and count != 0) or count == 8:
                    # launch a thread on the queue and get the result
                    # If the last word is PAUSE, but the length of the list is odd, send the words to the GPT API
                    if predicted_word == 'PAUSE' and len(words_predicted) % 2 != 0:
                        self.ui.prediction.q.put((words_predicted, self))
                    elif predicted_word != 'PAUSE':
                        self.ui.prediction.q.put((words_predicted, self))
                if predicted_word == 'PAUSE':
                # if count == 8:
                    words_predicted = []
                    self.ui.show_info("Fin de la phrase. Pour recommencer, appuyez sur le bouton Start.")
                    break

                print('***********************************************************')
                count += 1

            # If the data is a calibration message, print it so the user knows what is happening
            elif self.ui.prediction.right_serial_data.endswith('calibration AccGyro'):
                print('Calibration AccGyro en cours...')
                self.ui.show_info("Calibration AccGyro en cours...")
            elif self.ui.prediction.right_serial_data == 'Debut de calibration Flex':
                print('Calibration Flex en cours...')
                self.ui.show_info("Calibration Flex en cours...")
            elif self.ui.prediction.right_serial_data == 'Fin de calibration':
                print('Calibration terminee')
                self.ui.show_info("La calibration est terminee.\nL'enregistrement va commencer...")
            elif self.ui.prediction.right_serial_data == 'Debut Enregistrement...':
                print('Enregistrement en cours...')
                self.ui.show_info("Enregistrement en cours...")

        # Stop the queue
        self.ui.prediction.q.put(None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MagicGlovesUI()
    window.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
    window.show()
    sys.exit(app.exec_())
