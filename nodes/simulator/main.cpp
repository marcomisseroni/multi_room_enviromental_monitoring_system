#include <iostream>
#include "sensor_node_sim.hpp"

using namespace std;

int main() {

    mqtt_node::SensorNodeSim sensor_node_sim;
    sensor_node_sim.spin();

    return 0;
}