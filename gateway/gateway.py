import asyncio
from bleak import BleakClient
from bleak import BleakScanner
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import yaml

async def main():
    devices = await BleakScanner.discover()

    for d in devices:
        print(d.name, d.address)

asyncio.run(main())

'''
with open("../config/config_sim.yaml", "r") as file:
    config = yaml.safe_load(file)

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


p = Point("sensor_data").tag("room", room).tag("measurement_type", meas_type).field("value", float(msg.payload.decode()))
write_api.write(bucket=bucket, org=org, record=p)


def main():
    return


if __name__ == '__main__':
    main()
'''