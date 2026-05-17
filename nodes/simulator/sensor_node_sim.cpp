#include <iostream>
#include "mosquitto.h"
#include "sensor_node_sim.hpp"

using namespace std;
using namespace mqtt_node;

SensorNodeSim::SensorNodeSim() {
    
    mosquitto_lib_init();

}

