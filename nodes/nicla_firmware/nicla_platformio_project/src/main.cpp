#include <Arduino.h>
#include <ArduinoBLE.h>
#include <Arduino_BHY2.h>

// put function declarations here:
BLEService sensor_service("181A");
BLEFloatCharacteristic temp_char("2A6E", BLERead | BLENotify);
BLEFloatCharacteristic press_char("2A6D", BLERead | BLENotify);
Sensor temperature(SENSOR_ID_TEMP);
Sensor pressure(SENSOR_ID_BARO);
float temp;
float press;

void setup() {
  
  Serial.begin(115200);
  
  BHY2.begin();
  pressure.begin();
  temperature.begin();

  if(!BLE.begin()) {
    Serial.println("ERROR: Starting Bluetooth Low Energy module failed!");
    while(1);
  }

  BLE.setLocalName("NICLA_SENSOR");
  sensor_service.addCharacteristic(temp_char);
  sensor_service.addCharacteristic(press_char);

  BLE.setAdvertisedService(sensor_service);
  BLE.addService(sensor_service);
  BLE.advertise();

  Serial.println("BLE advertising...");
}

void loop() {
  BHY2.update();
  temp = temperature.value();
  press = pressure.value();
  temp_char.writeValue(temp);
  press_char.writeValue(press);
  delay(1000);
}

// put function definitions here: