cmake_minimum_required(VERSION 3.10)

project(iot_simulator)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(sensor_sim
    main.cpp
    sensor_node_sim.cpp
)

find_package(PkgConfig REQUIRED)
pkg_check_modules(MOSQUITTO REQUIRED libmosquitto)

include_directories(${MOSQUITTO_INCLUDE_DIRS})

target_link_libraries(sensor_sim
    mosquitto
    pthread
)