import struct
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import yaml
import signal
import asyncio
import contextlib
from typing import Iterable
import logging
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

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

# LOG
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# BLE
device1 = config["ble"]["device1"]
device2 = config["ble"]["device2"]
device3 =  config["ble"]["device3"]

uuid1_temp = config["ble"]["temp_uuid"]
uuid1_press = config["ble"]["press_uuid"]
uuid1_hum = config["ble"]["hum_uuid"]
uuid1_iaq = config["ble"]["air_q_uuid"]

uuid2_temp = config["ble"]["temp_uuid"]
uuid2_press = config["ble"]["press_uuid"]
uuid2_hum = config["ble"]["hum_uuid"]
uuid2_iaq = config["ble"]["air_q_uuid"]

uuid3_temp = config["ble"]["temp_uuid"]
uuid3_press = config["ble"]["press_uuid"]
uuid3_hum = config["ble"]["hum_uuid"]
uuid3_iaq = config["ble"]["air_q_uuid"]

# queue of values got from the devices
queue = asyncio.Queue()

def decode(data):
    if len(data) < 4:
        logger.warning("Data received is smaller than 4 bytes")
        return None
    return struct.unpack('<f', data[:4])[0]

# To avoid mismatch if the uuid is expressed in short or full 128-bit
def normalize_uuid(uuid: str) -> str:
    return uuid.lower().replace("-", "")


async def connect_to_device(
    lock: asyncio.Lock,
    name: str,
    notify_uuids: Iterable[str],
    shutdown_event: asyncio.Event,
):
    async with contextlib.AsyncExitStack() as stack:
        try:
            # Trying to establish a connection to two devices at the same time
            # can cause errors, so use a lock to avoid this.
            async with lock:
                device = await BleakScanner.find_device_by_name(name)

                if device is None:
                    logger.warning("Device %s not found", name)
                    return

                client = await stack.enter_async_context(BleakClient(device))
                logger.info("Connected to device %s", name)

            measurement_names = {
                normalize_uuid(config["ble"]["temp_uuid"]): "temperature",
                normalize_uuid(config["ble"]["press_uuid"]): "pressure",
                normalize_uuid(config["ble"]["hum_uuid"]): "humidity",
                normalize_uuid(config["ble"]["air_q_uuid"]): "air_quality",
            }

            def callback(measurement_type: str):
                def inner(_: BleakGATTCharacteristic, data: bytearray) -> None:
                    value = decode(data)
                    if value is None:
                        return

                    meas = measurement_names.get(
                        normalize_uuid(measurement_type),
                        measurement_type,
                    )
                    
                    p = (
                        Point("sensor_data")
                        .tag("room", name)
                        .tag("measurement_type", meas)
                        .field("value", value)
                    )
                    queue.put_nowait(p)

                return inner

            for notify_uuid in notify_uuids:
                try:
                    await client.start_notify(notify_uuid, callback(notify_uuid))
                    logger.info("Started notify %s for %s", notify_uuid, name)
                except Exception:
                    logger.exception("Failed to start notify %s for %s", notify_uuid, name)

            # Start notifications and wait until shutdown_event is set.
            try:
                await shutdown_event.wait()
            finally:
                # Ensure we always stop notifications before disconnecting.
                for notify_uuid in notify_uuids:
                    with contextlib.suppress(Exception):
                        await client.stop_notify(notify_uuid)

        except Exception:
            logger.exception("Error in connect_to_device for %s", name)
            return

async def influx_writer(shutdown_event: asyncio.Event):
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            if shutdown_event.is_set() and queue.empty():
                break
            continue

        try:
            write_api.write(bucket=bucket, org=org, record=item)
            logger.debug("Wrote point to InfluxDB: %s", item)
        except Exception:
            logger.exception("Failed to write on InfluxDB")
        finally:
            queue.task_done()

    # drain any remaining items (best-effort)
    while not queue.empty():
        item = await queue.get()
        try:
            write_api.write(bucket=bucket, org=org, record=item)
            logger.debug("Wrote point to InfluxDB: %s", item)
        except Exception:
            logger.exception("Failed to write on InfluxDB")
        finally:
            queue.task_done()

async def main(
    addresses: Iterable[str],
):
    lock = asyncio.Lock()
    shutdown_event = asyncio.Event()

    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGINT, shutdown_event.set)
        loop.add_signal_handler(signal.SIGTERM, shutdown_event.set)
    except NotImplementedError:
        # Signal handlers may not be implemented on some platforms
        pass

    writer_task = asyncio.create_task(influx_writer(shutdown_event))

    # Quick test write to InfluxDB to verify connectivity
    try:
        test_point = Point("sensor_data").tag("room", "gateway").tag("measurement_type", "startup_test").field("value", 1.0)
        write_api.write(bucket=bucket, org=org, record=test_point)
        logger.info("Successfully wrote startup test point to InfluxDB")
    except Exception:
        logger.exception("Startup write to InfluxDB failed")

    devices = [
        (device1, [uuid1_temp, uuid1_press, uuid1_hum, uuid1_iaq]),
        (device2, [uuid2_temp, uuid2_press, uuid2_hum, uuid2_iaq]),
        (device3, [uuid3_temp, uuid3_press, uuid3_hum, uuid3_iaq]),
    ]

    connect_tasks = []
    for address, uuids in devices:
        task = asyncio.create_task(
            connect_to_device(lock, address, uuids, shutdown_event)
        )
        connect_tasks.append(task)

    # Wait until all connect tasks complete (they wait on shutdown_event),
    # or until a signal sets shutdown_event.
    await asyncio.gather(*connect_tasks)

    # Ensure all queued points are written before exiting
    await queue.join()

    # Stop writer
    writer_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await writer_task

if __name__ == "__main__":
    # Run monitoring for temperature UUIDs of the three devices by default.
    addresses = (device1, device2, device3)

    try:
        asyncio.run(main(addresses))
    except KeyboardInterrupt:
        pass