#include <iostream>
#include <thread>
#include <chrono>
#include <string>
#include "sensor_node_sim.hpp"

using namespace std;

namespace mqtt_node {

    SensorNodeSim::SensorNodeSim(float temp_mean, float hum_mean, float press_mean, float air_qual_mean, 
                    float temp_std, float hum_std, float press_std, float air_qual_std) {

        // Initialize mosquitto library
        mosquitto_lib_init();

        // Parameters initialization
        _temperature_mean = temp_mean;
        _humidity_mean = hum_mean;
        _pressure_mean = press_mean;
        _air_quality_mean = air_qual_mean;
        _temperature_std = temp_std;
        _humidity_std = hum_std;
        _pressure_std = press_std;
        _air_quality_std = air_qual_std;
        _seed = 0;
        generator.seed(_seed);

        // Initialize mqtt client
        client = mosquitto_new("sensor_node", true, this);

        // mqtt callbacks
        mosquitto_connect_callback_set(client, on_connect_callback);
        mosquitto_disconnect_callback_set(client, on_disconnect_callback);
 
        // mqtt connection
        mosquitto_connect(client, "localhost", 1883, 60);
        mosquitto_loop_start(client);

    }

    SensorNodeSim::~SensorNodeSim() {
        mosquitto_disconnect(client);
        mosquitto_loop_stop(client, false);
    }

    void SensorNodeSim::set_seed(int new_seed) {
        _seed = new_seed;
    }

    void SensorNodeSim::generate_data() {
        std::normal_distribution<float> temp_dis(_temperature_mean, _temperature_std);
        std::normal_distribution<float> hum_dis(_humidity_mean, _humidity_std);
        std::normal_distribution<float> press_dis(_pressure_mean, _pressure_std);
        std::normal_distribution<float> air_q_dis(_air_quality_mean, _air_quality_std);

        float temp_reading = temp_dis(generator);
        float hum_reading = hum_dis(generator);
        float press_reading = press_dis(generator);
        float air_q_reading = air_q_dis(generator);

        publish_data(temp_reading, hum_reading, press_reading, air_q_reading);
    }

    int SensorNodeSim::publish_data(float temp, float hum, float press, float air_q) {

        string temp_payload = to_string(temp);
        string hum_payload = to_string(hum);
        string press_payload = to_string(press);
        string air_q_payload = to_string(air_q);

        mosquitto_publish(client, nullptr, _temp_topic, temp_payload.size(), temp_payload.c_str(), 2, true);
        mosquitto_publish(client, nullptr, _hum_topic, hum_payload.size(), hum_payload.c_str(), 2, true);
        mosquitto_publish(client, nullptr, _press_topic,press_payload.size(), press_payload.c_str(), 2, true);
        mosquitto_publish(client, nullptr, _air_q_topic, air_q_payload.size(), air_q_payload.c_str(), 2, true);

        // handle mqtt errors
        return 0;
    }

    void SensorNodeSim::spin() {

        while(true) {
            generate_data();
            std::this_thread::sleep_for(std::chrono::seconds(2));
        }
    }

    void SensorNodeSim::on_connect_callback(struct mosquitto *mosq, void *userdata, int rc) {
        cerr << "Connected rc = " << rc << endl;
    }

    void SensorNodeSim::on_disconnect_callback(struct mosquitto *mosq, void *userdata, int rc) {
        cerr << "Disconnected" << endl;
    }
}