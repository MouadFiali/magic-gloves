# Magic Gloves
## Description
"Magic Gloves" is an innovative project aimed at translating sign language into spoken language using smart gloves equipped with sensors. This technology captures the intricate movements and positions of sign language and translates them into words, bridging communication gaps for the deaf and hard-of-hearing community. Our GitHub repository documents the development journey, including data collection, machine learning models, and hardware-software integration, showcasing our commitment to enhancing accessibility through AI and IoT.

## Table of Contents
- [Data Collection](#data-collection)
- [Machine Learning Models](#machine-learning-models)
- [Hardware-Software Integration](#hardware-software-integration)
- [Notes](#notes)

## Data Collection
Unfortunately, we were unable to find a dataset containing the data of the sensors we used. Therefore, we had to collect our own data. We used the **Arduino Uno** along with flex sensors and an accelerometer/gyroscope to collect data.

In order to collect data, an arduino sketch was written to collect data from the sensors and send it to the serial monitor. Which is done by the file [`sensor_reader.ino`]("https://github.com/MouadFiali/magic-gloves/blob/main/sensor_reader/sensor_reader.ino"). Which includes a calibration phase to calibrate the sensors and a data collection phase to collect the data and write it as a comma separated values to make it easier to read by the python script.

The data is then read by the python script [`data_collector.py`]("https://github.com/MouadFiali/magic-gloves/blob/main/data_collection/data_collector.py") which reads the data from the serial monitor, formats it to fit the columns structure of the wanted dataset, and writes it to a csv file along with the label of the name of the sign. 

**Note:** The file [`dataset_initializer.py`]("https://github.com/MouadFiali/magic-gloves/blob/main/data_collection/dataset_initializer.py") is used to initialize the dataset by creating the csv file and writing the column names to it (441 columns which are the readings of the each used sensor for 20 frames, and the label column).

The dataset is uploaded to **Kaggle** and can be found [here](https://www.kaggle.com/datasets/mouadfiali/sensor-based-american-sign-language-recognition).

## Machine Learning Models
The machine learning models are trained using the dataset collected in the previous step.

3 models were trained:
- **Recurrent Neural Network**: Which is done by the file [`rnn.py`]("https://github.com/MouadFiali/magic-gloves/blob/main/models/rnn.py")
- **Long Short-Term Memory**: Which is done by the file [`lstm.py`]("https://github.com/MouadFiali/magic-gloves/blob/main/models/lstm.py")
- **Gated Recurrent Units**: Which is done by the file [`gru.py`]("https://github.com/MouadFiali/magic-gloves/blob/main/models/gru.py")

Each file contains the code for preprocessing the data, training the model, and testing the model. The models are then saved to be easily loaded and used in the next step.

## Hardware-Software Integration
The hardware-software integration is done using the python script [`predict.py`]("https://github.com/MouadFiali/magic-gloves/blob/main/predict.py") which loads the trained model and uses it to predict the sign being made by the user.

It is possible to use any of the 3 models trained in the previous step. The model to be used can be changed by changing the following line in the script:
```python
new_model = load_model('rnn_model.h5')
```

It reads the data from the serial monitor in a similar way to the data collection step, preprocesses it, and uses the model to predict the sign. This process is done in a loop to continuously predict the signs being made by the user.

As a first result, the models were able to predict the signs with a maximum shocking accuracy of **100%** for the **RNN** model. However, this result is not final and It probably is high due to the small size of the dataset.

The models were also able to predict the signs in real-time with no noticeable mistakes. However, the models are not yet ready to be used in real-life situations as they are still in the early stages of development.

## Notes
- This project is still under development and is not yet complete. We are still working on improving the models, the dataset, and the hardware-software integration.

- The dataset posted on Kaggle is not yet complete and is still being collected.

- This README file is not final and will be updated regularly to include more information about the project.

- In order to run the python scripts, you will need to change the ports names (numbers) in the scripts to match the port which the arduino is connected to. This can be done by changing the following lines in the scripts:
```python
# LEFT 
ser = serial.Serial('COM7', 9600)
# RIGHT
ser2 = serial.Serial('COM4', 9600)
```
