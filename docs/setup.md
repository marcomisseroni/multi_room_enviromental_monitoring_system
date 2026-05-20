# Setup Guide

## Requirements

- Raspberry Pi (Linux)
- Python 3.10+
- MQTT broker (Mosquitto)
- InfluxDB

---

## 1. Install MQTT broker

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```
## 2. Install InfluxDB

```bash
sudo apt install influxdb
```

## 3. Verify services

```bash
sudo systemctl start influxdb
sudo systemctl start mosquitto

sudo systemctl status influxdb
sudo systemctl status mosquitto.service
```