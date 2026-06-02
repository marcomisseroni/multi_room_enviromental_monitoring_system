#include <iostream>
#include <thread>
#include "sensor_node_sim.hpp"
 #include "gateway_sim.hpp"

using namespace std;

int main() {

    mqtt_node::SensorNodeSim sensor_node_sim1("NICLA_ROOM1");
    mqtt_node::SensorNodeSim sensor_node_sim2("NICLA_ROOM2");
    mqtt_node::SensorNodeSim sensor_node_sim3("NICLA_ROOM3");

    thread t1(&mqtt_node::SensorNodeSim::spin, &sensor_node_sim1);
    thread t2(&mqtt_node::SensorNodeSim::spin, &sensor_node_sim2);
    thread t3(&mqtt_node::SensorNodeSim::spin, &sensor_node_sim3);

    t1.join();
    t2.join();
    t3.join();

    return 0;
}