#!/bin/bash 

echo "----------------------Welcome to the IoT project simulation----------------------" 
echo "Author: Marco Misseroni"

# activate the virtual enviroment
if [ -d "venv" ]; then
    echo "Virtual environment found"
    echo "Activating virtual enviroment"
else
    echo "ERROR: venv not found"
    echo "Creating a new virtual enviroment..."
    python3 -m venv venv
    pip install -r requirements.txt
fi

source venv/bin/activate

# activate mosquitto broker
echo "Starting mosquitto broker..."
sudo systemctl start mosquitto

# activate influxdb via docker
docker start influxdb

# activate grafana
sudo systemctl start grafana-server

cd nodes/simulator

echo "Building the project..."

cmake -B build
cmake --build build

echo "executing the nodes..."

./build/sensor_sim &
SENSOR_PID=$!

python3 gateway_sim.py &
GATEAWY_PID=$!

# open grafana UI
echo "Opening grafana dashboard"
xdg-open http://localhost:3000/d/adml8zm/iot-project?orgId=1&from=now-5m&to=now&timezone=browser

cleanup() {
    echo "Stopping system..."
    kill $SENSOR_PID $GATEAWY_PID
}

trap cleanup SIGINT

wait