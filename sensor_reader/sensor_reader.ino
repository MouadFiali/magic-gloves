// These constants won't change:
const int sensorPins[] = {A0, A1, A2, A3, A4};  // pins that the sensors are attached to

// variables:
int sensorValues[5] = {0, 0, 0, 0, 0};   // the sensor values
int sensorMins[5] = {1023, 1023, 1023, 1023, 1023};  // minimum sensor values
int sensorMaxs[5] = {0, 0, 0, 0, 0};     // maximum sensor values


void setup() {

    Serial.begin(9600);
    Serial.print("Debut de calbiration");

    // calibrate during the first five seconds
    while (millis() < 20000) {
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

     Serial.print("Fin de calbiration");

    for (int i = 0; i < 5; i++) {
        Serial.print("SenserValue du flex ");
        Serial.print(i);
        Serial.print(" : ");
        Serial.println(sensorMins[i]);


        Serial.print("Max du flex ");
        Serial.print(i);
        Serial.print(" : ");
        Serial.println(sensorMaxs[i]);

        Serial.print("Min du flex ");
        Serial.print(i);
        Serial.print(" : ");
        Serial.println(sensorMins[i]);
    }
            



   
}

void loop() {
    for (int i = 0; i < 5; i++) {
        // read the sensor:
        sensorValues[i] = analogRead(sensorPins[i]);

        // in case the sensor value is outside the range seen during calibration
        sensorValues[i] = constrain(sensorValues[i], sensorMins[i], sensorMaxs[i]);

        // apply the calibration to the sensor reading
        sensorValues[i] = map(sensorValues[i], sensorMins[i], sensorMaxs[i], 0, 255);

        Serial.print("Valeur du capteur de flexion ");
        Serial.print(i);
        Serial.print(" : ");
        Serial.println(sensorValues[i]);

        delay(1000); // Attendre 1 seconde (ajustez selon vos besoins)


    }
}