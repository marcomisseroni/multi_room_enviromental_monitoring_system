import random
from paho.mqtt import client as mqtt_client
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

# mqtt variables
broker = 'localhost'
port = 1883
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

# influxdb variables
# username: marco
# password: password
bucket = "sensor_data"
org = "iot_project"
token = "NG8aNfKB4ETV9sXsrDPW4Nnxdl6C5Q5yhagI3PwEnw_eKua1T5fKSpy0fR0Wv8Fpz9IITi3pN83RdQg1S5iPMA=="
url="http://localhost:8086"

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
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
    )
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    #try: 
    client.connect(broker, port)
    #except Exception as e:
    #    print(f"TCP connection failed: {e}")
    #    client.disconnect()
    #    client = None

    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        home, room, meas_type = msg.topic.split("/")
        p = Point("sensor_data").tag("room", room).tag("measurement_type", meas_type).field("value", float(msg.payload.decode()))
        write_api.write(bucket=bucket, org=org, record=p)

    client.subscribe("home/#")
    client.on_message = on_message


def run():
    client_mqtt = connect_mqtt()
    if client_mqtt is None:
        return
    subscribe(client_mqtt)
    client_mqtt.loop_forever()


if __name__ == '__main__':
    run()
