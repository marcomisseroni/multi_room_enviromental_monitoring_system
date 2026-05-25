#include <Arduino.h>
#include <ArduinoBLE.h>

// put function declarations here:
//int myFunction(int, int);

void setup() {
  Serial.begin(115200);
  if(!BLE.begin()) {
    Serial.println("ERROR: Starting Bluetooth Low Energy module failed!");
  }
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("loop");
  delay(1000);
}

// put function definitions here: