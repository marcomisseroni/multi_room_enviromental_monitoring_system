#include <iostream>
#include "gateway_sim.hpp"

using namespace std;

namespace mqtt_node {

    GatewaySim::GatewaySim() {

        mosquitto_lib_init();

        client = mosquitto_new("gateway_node", true, this);

        if(client == NULL) {
            cerr << "Error: Couldn't initialize mosquitto struct" << endl;
            return;
        }

        // mqtt callbacks
        mosquitto_connect_callback_set(client, on_connect_callback);
        mosquitto_disconnect_callback_set(client, on_disconnect_callback);
        mosquitto_message_callback_set(client, on_message);
 
        // mqtt connection
        mosquitto_connect(client, "192.168.1.17", 1883, 60);
        mosquitto_loop_start(client);

        mosquitto_subscribe(client, nullptr, "temperature_sensor", 2);
        mosquitto_subscribe(client, nullptr, "humidity_sensor", 2);
        mosquitto_subscribe(client, nullptr, "pressure_sensor", 2);
        mosquitto_subscribe(client, nullptr, "air_quality_sensor", 2);
        
    }

    GatewaySim::~GatewaySim() {
        mosquitto_disconnect(client);
        mosquitto_loop_stop(client, false);
    }

    void GatewaySim::on_connect_callback(struct mosquitto *mosq, void *userdata, int rc) {
        cerr << "Connected rc = " << rc << endl;
    }

    void GatewaySim::on_disconnect_callback(struct mosquitto *mosq, void *userdata, int rc) {
        cerr << "Disconnected" << endl;
    }

    void GatewaySim::spin() {

        while(true) {}

    }

    void GatewaySim::on_message(mosquitto *mosq, void *userdata, const struct mosquitto_message *message) {

        cerr << "[Gateway] " << "Topic: " << message->topic << "Payload: " << string((char*)message->payload, message->payloadlen) << endl;

    }

}