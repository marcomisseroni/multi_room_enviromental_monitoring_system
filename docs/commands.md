# Build from `nodes/simulator`

Cmake is used, so as usual:

```
cmake -B build

```
to create the build directory and then:

```
cmake --build build
```
to build.

Before launching the program recall to start the MQTT broker using:

```
sudo systemctl start mosquitto
```
you can also check if the broker is running using `sudo systemctl status mosquitto.service`.

After starting the broker you can launch the node using:

```
./build/sensor_sim
```

To stop the broker you can use:

```
sudo systemctl stop mposquitto
```