#include "LSM6DS3.h"
#include "Wire.h"

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A

// These constants won't change:
const int sensorPins[] = {A0, A1, A2, A3, A4};  // pins that the sensors are attached to

// variables:
int sensorValues[5] = {0, 0, 0, 0, 0};   // the sensor values
int sensorMins[5] = {1023, 1023, 1023, 1023, 1023};  // minimum sensor values
int sensorMaxs[5] = {0, 0, 0, 0, 0};     // maximum sensor values
int numReadings = 0 ;

// Variables pour stocker les valeurs de calibration
float accelOffset[3] = {0, 0, 0};
float gyroOffset[3] = {0, 0, 0};

void setup() {

    Serial.begin(9600);
    myIMU.begin();
    Serial.println("Debut de calibration");
    // calibrate during the first 20 seconds
    while (millis() < 20000) {
        numReadings = numReadings +1 ;
        // Flex sensors
        for (int i = 0; i < 5; i++) {
            sensorValues[i] = analogRead(sensorPins[i]);

            // record the maximum sensor value
            if (sensorValues[i] > sensorMaxs[i]) {
                sensorMaxs[i] = sensorValues[i];
            }

            // record the minimum sensor value
            if (sensorValues[i] < sensorMins[i]) {
                sensorMins[i] = sensorValues[i];
            }
        }

        // Accelerometer
        accelOffset[0] += myIMU.readFloatAccelX();
        accelOffset[1] += myIMU.readFloatAccelY();
        accelOffset[2] += myIMU.readFloatAccelZ();

        // Gyro
        gyroOffset[0] += myIMU.readFloatGyroX();
        gyroOffset[1] += myIMU.readFloatGyroY();
        gyroOffset[2] += myIMU.readFloatGyroZ();

    }


    accelOffset[0] /= numReadings;
    accelOffset[1] /= numReadings;
    accelOffset[2] -= 1.0;
    gyroOffset[0] /= numReadings;
    gyroOffset[1] /= numReadings;
    gyroOffset[2] /= numReadings;

    Serial.println("Fin de calibration");
}

void loop() {
    Serial.println("Debut Enregistrement...");
    // In 2 seconds, we should record 10 frames
    unsigned long time = millis();
    for(int j = 0; j < 20; j++){
      // delay time
      unsigned long delayTime = millis();

      // Flex
      for (int i = 0; i < 5; i++) {
        // read the sensor:
        sensorValues[i] = analogRead(sensorPins[i]);
        // in case the sensor value is outside the range seen during calibration
        sensorValues[i] = constrain(sensorValues[i], sensorMins[i], sensorMaxs[i]);
        // apply the calibration to the sensor reading
        sensorValues[i] = map(sensorValues[i], sensorMins[i], sensorMaxs[i], 0, 255);
        Serial.print(sensorValues[i]);
        Serial.print(",");
      }
      // Accelerometer
      float accelX = myIMU.readFloatAccelX() - accelOffset[0];
      float accelY = myIMU.readFloatAccelY() - accelOffset[1];
      float accelZ = myIMU.readFloatAccelZ() - accelOffset[2];
      Serial.print(accelX);
      Serial.print(",");
      Serial.print(accelY);
      Serial.print(",");
      Serial.print(accelZ);
      Serial.print(",");

      // Gyro
      float gyroX = myIMU.readFloatGyroX() - gyroOffset[0];
      float gyroY = myIMU.readFloatGyroY() - gyroOffset[1];
      float gyroZ = myIMU.readFloatGyroZ() - gyroOffset[2];
      Serial.print(gyroX);
      Serial.print(",");
      Serial.print(gyroY);
      Serial.print(",");
      Serial.print(gyroZ);
      Serial.print(",");
      

      delayTime = millis() - delayTime;
      if(delayTime < 150){
        delay(150 - delayTime);
      }
    }
    Serial.println("");
    // Serial.print("Execution time: ");
    // Serial.println(millis() - time);


    delay(3850); // Wait for 4 second before reading again
}