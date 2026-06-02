import random
from paho.mqtt import client as mqtt_client
from paho.mqtt.subscribeoptions import SubscribeOptions
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import yaml

with open("../../config/config_sim.yaml", "r") as file:
    config = yaml.safe_load(file)


# mqtt variables
broker = config["mqtt"]["broker_ip"]
port = config["mqtt"]["port"]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

# influxdb variables
# username: marco
# password: password
bucket = config["influxdb"]["bucket"]
org = config["influxdb"]["org"]
token = config["influxdb"]["token"]
url="http://" + config["influxdb"]["ip"] + ":" + str(config["influxdb"]["port"])

client_influxdb = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

write_api = client_influxdb.write_api(write_options=SYNCHRONOUS)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {reason_code}")

    client = mqtt_client.Client(
        client_id=client_id,
        protocol=mqtt_client.MQTTv5,
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
    )
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        home, room, meas_type = msg.topic.split("/")
        p = Point("sensor_data").tag("room", room).tag("measurement_type", meas_type).field("value", float(msg.payload.decode()))
        write_api.write(bucket=bucket, org=org, record=p)

    client.subscribe("home/#", options=SubscribeOptions(qos=1, retainHandling=2))
    client.on_message = on_message


def run():
    client_mqtt = connect_mqtt()
    if client_mqtt is None:
        return
    subscribe(client_mqtt)
    client_mqtt.loop_forever()


if __name__ == '__main__':
    run()
