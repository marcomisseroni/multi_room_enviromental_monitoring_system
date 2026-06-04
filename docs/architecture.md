# System Architecture

## Overview
Distributed IoT system for environmental monitoring using BLE sensors and Raspberry Pi gateway.

---

## Components

### Sensor Nodes (Nicla Sense ME)
- Measure temperature, humidity, pressure, air quality
- Send data via BLE

### Raspberry Pi Gateway
- Collects data from all nodes
- Processes and normalizes data
- Stores data locally

### Database
- Stores time-series environmental data
- InfluxDB

### Dashboard
- Visualizes real-time and historical data
- Grafana

---

## Data Flow

Sensor Node → BLE → Gateway → Database → Dashboard

---

## Communication Protocols

- BLE for sensor node → gateway communication
- MQTT for data transmission during the simulation phase
- HTTP for database communication (InfluxDB API)
- HTTP for dashboard data retrieval and visualization (Grafana API)