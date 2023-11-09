#include "LSM6DS3.h"
#include "Wire.h"

LSM6DS3 myIMU(I2C_MODE, 0x6A);
const int capteurPin1 = A0;
const int capteurPin2 = A1;
const int capteurPin3 = A2;
const int capteurPin4 = A3;
const int capteurPin5 = A4;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  myIMU.begin();
}

void loop() {
  int valeurCapteur1 = analogRead(capteurPin1);
  int valeurCapteur2 = analogRead(capteurPin2);
  int valeurCapteur3 = analogRead(capteurPin3);
  int valeurCapteur4 = analogRead(capteurPin4);
  int valeurCapteur5 = analogRead(capteurPin5);

  Serial.print(myIMU.readFloatAccelX(), 4);
  Serial.print(",");
  Serial.print(myIMU.readFloatAccelY(), 4);
  Serial.print(",");
  Serial.print(myIMU.readFloatAccelZ(), 4);
  Serial.print(",");
  Serial.print(valeurCapteur1);
  Serial.print(",");
  Serial.print(valeurCapteur2);
  Serial.print(",");
  Serial.print(valeurCapteur3);
  Serial.print(",");
  Serial.print(valeurCapteur4);
  Serial.print(",");
  Serial.print(valeurCapteur5);
  Serial.println();  // End of the line

  delay(1000);
}
