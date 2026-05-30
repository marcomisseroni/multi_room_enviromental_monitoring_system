echo "---------------------- Flash firmware for NICLA SENSE ME ----------------------" 

cd nodes/nicla_firmware/nicla_platformio_project

pio run -e nicla_room3 -t upload

#pio device monitor -b 115200