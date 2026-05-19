#ifndef GATEWAY_SIM_HPP
#define GATEWAY_SIM_HPP

#include <mosquitto/libmosquitto.h>

namespace mqtt_node {

    class GatewaySim {

        public:

            GatewaySim();
            ~GatewaySim();
            void spin();

        private:

            mosquitto *client;

            static void on_connect_callback(struct mosquitto *mosq, void *userdata, int rc);
            static void on_disconnect_callback(struct mosquitto *mosq, void *userdata, int rc);

            static void on_message(mosquitto *mosq, void *userdata, const struct mosquitto_message *message);
    };
}

#endif // gateway_sim.hpp