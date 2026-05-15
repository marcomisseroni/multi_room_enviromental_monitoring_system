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

### Dashboard
- Visualizes real-time and historical data

---

## Data Flow

Sensor Node → BLE → Gateway → Database → Dashboard

---

## Communication Protocols

- BLE for node → gateway communication
- MQTT (optional in simulation phase)
- HTTP for dashboard API

---

## System Diagram

(Add image here)