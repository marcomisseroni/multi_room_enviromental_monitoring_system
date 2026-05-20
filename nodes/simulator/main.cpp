#include <iostream>
#include "sensor_node_sim.hpp"
 #include "gateway_sim.hpp"

using namespace std;

int main() {

    mqtt_node::SensorNodeSim sensor_node_sim1("room1");
    mqtt_node::SensorNodeSim sensor_node_sim2("room2");
    mqtt_node::SensorNodeSim sensor_node_sim3("room3");

    sensor_node_sim1.spin();
    sensor_node_sim2.spin();
    sensor_node_sim3.spin();

    return 0;
}