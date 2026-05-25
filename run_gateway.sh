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

cd gateway

# activate the build-in bluetooth (to download the pkg: sudo apt-get install bluetooth bluez)
sudo hciconfig hci0 up

python3 gateway.py &
GATEAWY_PID=$!

cleanup() {
    echo "Stopping system..."
    kill $GATEAWY_PID
}

trap cleanup SIGINT

wait