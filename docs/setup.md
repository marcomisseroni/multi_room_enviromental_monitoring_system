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

Alternatively you can set up a docker container with Influxdb. 
First of all install docker using: `sudo apt install docker.io`.
Then you can create the container for Influxdb using:

```bash
docker run -d --name influxdb -p 8086:8086 -v influxdb-data:/var/lib/influxdb2 influxdb:2
```
Other useful commands to run an existing contaier, to list all containers, active containers, stop a container, delete a container:

```bash
docker start <container_name>
docker ps -a
docker ps
docker stop <container_name>
docker rm <container_name>
```

## 3. Verify services

If you run InfluxDB on docker you don't need to verify the service.

```bash
sudo systemctl start influxdb
sudo systemctl start mosquitto

sudo systemctl status influxdb
sudo systemctl status mosquitto.service
```

## 4. Initialize InfluxDB

Write in the browser:

```bash
http://localhost:8086
```

you can use the ip where the InlfuxDB service is running instead of `localhost`.
Then log in with your `name` and `password` then insert the `organization` and `bucket` that should match the info in the gateway python script. Then generate a new `token` or use an old one, then assign it to the token variable in the gateway script.