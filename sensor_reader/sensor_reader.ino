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

float accelValue[3] = {0, 0, 0}; // The accelerometer values
float accelMin[3] = {1023, 1023, 1023}; // Minimum accelerometer values
float accelMax[3] = {0, 0, 0}; // Maximum accelerometer values

float gyroValue[3] = {0, 0, 0}; // The gyro values
float gyroMin[3] = {1023, 1023, 1023}; // Minimum gyro values
float gyroMax[3] = {0, 0, 0}; // Maximum gyro values

void setup() {

    Serial.begin(9600);
    myIMU.begin();
    Serial.println("Debut de calibration");

    // calibrate during the first 20 seconds
    while (millis() < 20000) {
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
        accelValue[0] = myIMU.readFloatAccelX();
        accelValue[1] = myIMU.readFloatAccelY();
        accelValue[2] = myIMU.readFloatAccelZ();
        for (int i = 0; i < 3; i++){
          // record the max accel values
          if(accelValue[i] > accelMax[i]){
            accelMax[i] = accelValue[i];
          }

          // record the min accel values
          if(accelValue[i] < accelMin[i]){
            accelMin[i] = accelValue[i];
          }
        }

        // Gyro
        gyroValue[0] = myIMU.readFloatGyroX();
        gyroValue[1] = myIMU.readFloatGyroY();
        gyroValue[2] = myIMU.readFloatGyroZ();
        for (int i = 0; i < 3; i++){
          // record the max gyro values
          if(gyroValue[i] > gyroMax[i]){
            gyroMax[i] = gyroValue[i];
          }

          // record the min gyro values
          if(gyroValue[i] < gyroMin[i]){
            gyroMin[i] = gyroValue[i];
          }
        }
    }

    Serial.println("Fin de calibration");
}

void loop() {
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
      accelValue[0] = myIMU.readFloatAccelX();
      accelValue[1] = myIMU.readFloatAccelY();
      accelValue[2] = myIMU.readFloatAccelZ();
      for (int i = 0; i < 3; i++){
        accelValue[i] = constrain(accelValue[i], accelMin[i], accelMax[i]);
        accelValue[i] = map(accelValue[i], accelMin[i], accelMax[i], -50, 50);
        Serial.print(accelValue[i]);
        Serial.print(",");
      }
      // Gyro
      gyroValue[0] = myIMU.readFloatGyroX();
      gyroValue[1] = myIMU.readFloatGyroY();
      gyroValue[2] = myIMU.readFloatGyroZ();
      for (int i = 0; i < 3; i++){
        gyroValue[i] = constrain(gyroValue[i], gyroMin[i], gyroMax[i]);
        gyroValue[i] = map(gyroValue[i], gyroMin[i], gyroMax[i], -50, 50);
        Serial.print(gyroValue[i]);
        Serial.print(",");
      }

      delayTime = millis() - delayTime;
      if(delayTime < 100){
        delay(100 - delayTime);
      }
    }
    Serial.println("");
    // Serial.print("Execution time: ");
    // Serial.println(millis() - time);


    delay(1900); // Wait for 1 second before reading again
}