import asyncio
from bleak import BleakClient
from bleak import BleakScanner
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import yaml

'''
# INFLUXDB
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
'''
# BLUETOOTH LOW ENERGY
DEVICE_NAME = "NICLA_SENSOR"
MODEL_NBR_UUID = "2A6E"


#p = Point("sensor_data").tag("room", room).tag("measurement_type", meas_type).field("value", float(msg.payload.decode()))
#write_api.write(bucket=bucket, org=org, record=p)

'''
def main():
    return


if __name__ == '__main__':
    main()

'''
    
import asyncio
import struct
from bleak import BleakClient

address = "69:29:AE:F3:75:10"
PRESSURE_UUID = "2A6E"

def callback(sender, data):
    pressure = struct.unpack('<f', data)[0]
    print("Pressure:", pressure)

async def main():
    async with BleakClient(address) as client:
        await client.start_notify(PRESSURE_UUID, callback)

        while True:
            await asyncio.sleep(1)

asyncio.run(main())