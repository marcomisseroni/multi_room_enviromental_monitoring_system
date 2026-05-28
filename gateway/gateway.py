import struct
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import yaml
import argparse
import signal
import asyncio
import contextlib
import logging
from typing import Iterable

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

# BLE
device1 = "NICLA_ROOM1"
device2 = "NICLA_ROOM2"
device3 =  "NICLA_ROOM3"

uuid1_temp = "2A6E"
uuid1_press = "2A6D"
uuid1_hum = "2A6F"

uuid2_temp = "2A6E"
uuid2_press = "2A6D"
uuid2_hum = "2A6F"

uuid3_temp = "2A6E"
uuid3_press = "2A6D"
uuid3_hum = "2A6F"


queue = asyncio.Queue()

def decode(data):
    if len(data) < 4:
        return None
    return struct.unpack('<f', data[:4])[0]


async def connect_to_device(
    lock: asyncio.Lock,
    name_or_address: str,
    notify_uuid: str,
    shutdown_event: asyncio.Event,
):
    async with contextlib.AsyncExitStack() as stack:
        try:
            # Trying to establish a connection to two devices at the same time
            # can cause errors, so use a lock to avoid this.
            async with lock:
                device = await BleakScanner.find_device_by_name(name_or_address)

                if device is None:
                    return

                client = await stack.enter_async_context(BleakClient(device))

            def callback(_: BleakGATTCharacteristic, data: bytearray) -> None:
                value = decode(data)
                if value is None:
                    return
                p = (
                    Point("sensor_data")
                    .tag("room", name_or_address)
                    .tag("measurement_type", notify_uuid)
                    .field("value", value)
                )
                queue.put_nowait(p)

            # Start notifications and wait until shutdown_event is set.
            try:
                await client.start_notify(notify_uuid, callback)
                await shutdown_event.wait()
            finally:
                # Ensure we always stop notifications before disconnecting.
                try:
                    await client.stop_notify(notify_uuid)
                except Exception:
                    return

        except Exception:
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
        except Exception:
            print("ERROR: Failed to write on Influxdb")
        finally:
            queue.task_done()

    # drain any remaining items (best-effort)
    while not queue.empty():
        item = await queue.get()
        try:
            write_api.write(bucket=bucket, org=org, record=item)
        except Exception:
            print("ERROR: Failed to write on Influxdb")
        finally:
            queue.task_done()

async def main(
    addresses: Iterable[str],
    uuids: Iterable[str],
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

    connect_tasks = [
        asyncio.create_task(connect_to_device(lock, address, uuid, shutdown_event))
        for address, uuid in zip(addresses, uuids)
    ]

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
    uuids = (uuid1_temp, uuid2_temp, uuid3_temp)

    try:
        asyncio.run(main(addresses, uuids))
    except KeyboardInterrupt:
        pass