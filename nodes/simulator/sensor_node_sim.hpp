// SensorNodeSim.hpp
#ifndef SENSOR_NODE_SIM_HPP
#define SENSOR_NODE_SIM_HPP

#include <mosquitto/libmosquittopp.h>

namespace mqtt_node {

    class SensorNodeSim : public mosqpp::mosquittopp {

        public:

            SensorNodeSim(float temp_mean = 20, float hum_mean = 40, float press_mean = 1013, float air_qual_mean = 100, 
                float temp_std = 2, float hum_std = 10, float press_std = 20, float air_qual_std = 20);
            ~SensorNodeSim();

            void set_seed(int new_seed);

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
            const char *_temp_topic = "temperature_sensor";
            const char *_hum_topic = "humidity_sensor";
            const char *_press_topic = "pressure_sensor";
            const char *_air_q_topic = "air_quality_sensor";

            void generate_data();
            int publish_data(float temp, float hum, float press, float air_q);
            void on_connect(int rc) override;
            void on_disconnect(int rc) override;

    };

}

#endif // SensorNodeSim.hpp