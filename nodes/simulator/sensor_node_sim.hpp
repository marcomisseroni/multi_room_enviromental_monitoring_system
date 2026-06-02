// SensorNodeSim.hpp
#ifndef SENSOR_NODE_SIM_HPP
#define SENSOR_NODE_SIM_HPP

#include <random>
#include <mosquitto/libmosquitto.h>
#include <string>


namespace mqtt_node {

    class SensorNodeSim {

        public:

            SensorNodeSim(std::string room_name, float temp_mean = 20, float hum_mean = 40, float press_mean = 1013, float air_qual_mean = 100, 
                float temp_std = 2, float hum_std = 10, float press_std = 20, float air_qual_std = 20);
            ~SensorNodeSim();

            void set_seed(int new_seed);
            void spin();

        private:

            float _temperature_mean;
            float _humidity_mean;
            float _pressure_mean;
            float _air_quality_mean;
            float _temperature_std;
            float _humidity_std;
            float _pressure_std;
            float _air_quality_std;
            int _seed;
            std::string _temp_topic = "temperature";
            std::string _hum_topic = "humidity";
            std::string _press_topic = "pressure";
            std::string _air_q_topic = "air_quality";
            std::string _room_name;
            int _room_id;
            std::default_random_engine generator;
            
            inline static int _room_count = 0;

            mosquitto *client;

            void generate_data();
            int publish_data(float temp, float hum, float press, float air_q);
            static void on_connect_callback(struct mosquitto *mosq, void *userdata, int rc);
            static void on_disconnect_callback(struct mosquitto *mosq, void *userdata, int rc);
    };

}

#endif // SensorNodeSim.hpp