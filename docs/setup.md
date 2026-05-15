# Setup Guide

## Requirements

- Raspberry Pi (Linux)
- Python 3.10+
- MQTT broker (Mosquitto)

---

## 1. Install MQTT broker

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto