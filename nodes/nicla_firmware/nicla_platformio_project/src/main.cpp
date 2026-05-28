#include <Arduino.h>
#include <ArduinoBLE.h>
#include <Arduino_BHY2.h>

#ifndef DEVICE_NAME
#define DEVICE_NAME "NICLA_DEFAULT"
#endif

BLEService sensor_service("181A");
BLEFloatCharacteristic temp_char("2A6E", BLERead | BLENotify);
BLEFloatCharacteristic press_char("2A6D", BLERead | BLENotify);
BLEFloatCharacteristic hum_char("2A6F", BLERead | BLENotify);
Sensor temperature(SENSOR_ID_TEMP);
Sensor pressure(SENSOR_ID_BARO);
Sensor humidity(SENSOR_ID_HUM);
float temp;
float press;
float hum;

void setup() {
  
  Serial.begin(115200);
  
  BHY2.begin(); // initialize BHY2 sensor (temperature, pressure, humidity)
  pressure.begin();
  temperature.begin();
  humidity.begin();

  if(!BLE.begin()) {
    Serial.println("ERROR: Starting Bluetooth Low Energy module failed!");
    while(1);
  }

  BLE.setLocalName(DEVICE_NAME);
  sensor_service.addCharacteristic(temp_char);
  sensor_service.addCharacteristic(press_char);
  sensor_service.addCharacteristic(hum_char);

  BLE.setAdvertisedService(sensor_service);
  BLE.addService(sensor_service);
  BLE.advertise();

  Serial.println("BLE advertising...");
}

void loop() {
  BHY2.update();
  temp = temperature.value();
  press = pressure.value();
  hum = humidity.value();
  temp_char.writeValue(temp);
  press_char.writeValue(press);
  hum_char.writeValue(hum);
  delay(1000);
}
