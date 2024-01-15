#include "LSM6DS3.h"
#include "Wire.h"
#define sensitivity 8.75

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
float RateRoll, RatePitch, RateYaw;
float RateCalibrationRoll, RateCalibrationPitch, RateCalibrationYaw;
float AccX, AccY, AccZ;
float AccCalibrationX, AccCalibrationY, AccCalibrationZ;
int calibrationNumber = 0;

void readAccGyro(void) {
    // Read gyro values from LSM6DS3
    RateRoll = myIMU.readFloatGyroX() / sensitivity;
    RatePitch = myIMU.readFloatGyroY() / sensitivity;
    RateYaw = myIMU.readFloatGyroZ() / sensitivity;

    // Read accelerometer values
    AccX = myIMU.readFloatAccelX();
    AccY = myIMU.readFloatAccelY();
    AccZ = myIMU.readFloatAccelZ();
}

void setup() {

    Serial.begin(9600);
    Wire.begin();
    myIMU.begin();

    // Calibrate the sensors
    RateCalibrationRoll = RateCalibrationPitch = RateCalibrationYaw = 0;
    AccCalibrationX = AccCalibrationY = AccCalibrationZ = 0;

    Serial.println("Debut de calibration AccGyro");
    unsigned long time = millis();
    // calibrate during the first 20 seconds
    while (millis() - time < 10000) {
      calibrationNumber++;
      readAccGyro();
      RateCalibrationRoll += RateRoll;
      RateCalibrationPitch += RatePitch;
      RateCalibrationYaw += RateYaw;
      AccCalibrationX += AccX;
      AccCalibrationY += AccY;
      AccCalibrationZ += AccZ;
      delay(1);
    }

    RateCalibrationRoll /= calibrationNumber;
    RateCalibrationPitch /= calibrationNumber;
    RateCalibrationYaw /= calibrationNumber;
    AccCalibrationX /= calibrationNumber;
    AccCalibrationY /= calibrationNumber;
    AccCalibrationZ /= calibrationNumber;

    Serial.println("Debut de calibration Flex");

    time = millis();
    while (millis() - time < 10000) {
        numReadings++;
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
    }

    Serial.println("Fin de calibration");
}

void loop() {
    delay(2000); // Wait for 2 second before reading again
    
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
      
      readAccGyro();
    
      // Subtract calibration values from the current reading
      RateRoll -= RateCalibrationRoll;
      RatePitch -= RateCalibrationPitch;
      RateYaw -= RateCalibrationYaw;
      AccX -= AccCalibrationX;
      AccY -= AccCalibrationY;
      AccZ -= AccCalibrationZ;

      // Acceleration (Position wannabe)
      Serial.print(RateRoll);
      Serial.print(",");
      Serial.print(RatePitch);
      Serial.print(",");
      Serial.print(RateYaw);
      Serial.print(",");

      // Orientation (GYRO)
      Serial.print(AccX);
      Serial.print(",");
      Serial.print(AccY);
      Serial.print(",");
      Serial.print(AccZ);
      Serial.print(",");
      

      delayTime = millis() - delayTime;
      if(delayTime < 150){
        delay(150 - delayTime);
      }
    }
    Serial.println("");
    // Serial.print("Execution time: ");
    // Serial.println(millis() - time);


}