#include <iostream>
#include "sensor_node_sim.hpp"
 #include "gateway_sim.hpp"

using namespace std;

int main() {

    mqtt_node::SensorNodeSim sensor_node_sim;
    mqtt_node::GatewaySim gateway_sim;

    sensor_node_sim.spin();
    gateway_sim.spin();

    return 0;
}