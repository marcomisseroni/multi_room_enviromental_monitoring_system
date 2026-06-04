# Multi-Room Environmental Monitoring System

This project implements a distributed IoT system for environmental monitoring using multiple Arduino Nicla Sense ME nodes deployed in different rooms and a central Raspberry Pi gateway.

The system collects environmental data (temperature, humidity, pressure, and air quality) from multiple sensor nodes using Bluetooth Low Energy (BLE), stores the data locally on the Raspberry Pi, and provides both real-time and historical visualization through a web dashboard.

---

## System Architecture

The system is composed of:

- **Sensor Nodes (Arduino Nicla Sense ME)**
  - Collect environmental data
  - Send data via BLE

- **Raspberry Pi Gateway**
  - Receives data from all nodes
  - Processes and stores data in a local database
  - Acts as central communication hub

- **Database**
  - Stores historical measurements (InfluxDB)

- **Dashboard**
  - Displays real-time and historical data
  - Web-based interface (Grafana)

---

## Communication

The system uses **Bluetooth Low Energy (BLE)** for communication between sensor nodes and the Raspberry Pi gateway.
It is also used HTTP for the API of InfluxDB and Grafana

---

## Features

- Multi-node environmental monitoring
- BLE-based data acquisition
- Local data storage on Raspberry Pi
- Real-time data visualization
- Historical data analysis
- Modular and scalable architecture

---
