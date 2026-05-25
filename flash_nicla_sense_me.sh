echo "---------------------- Flash firmware for NICLA SENSE ME ----------------------" 

cd nodes/nicla_firmware/nicla_platformio_project

pio run -t upload

pio device monitor -b 115200