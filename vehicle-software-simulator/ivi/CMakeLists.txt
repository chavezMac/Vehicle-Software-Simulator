cmake_minimum_required(VERSION 3.16)
project(ivi_dashboard LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 REQUIRED COMPONENTS Core Gui Qml Quick WebSockets)

add_executable(ivi_dashboard
    src/main.cpp
    src/VehicleStateModel.cpp
    src/VehicleStateModel.h
    src/GatewayClient.cpp
    src/GatewayClient.h
    qml/qml.qrc      # if you bundle QML via resource file
)

target_link_libraries(ivi_dashboard
    Qt5::Core
    Qt5::Gui
    Qt5::Qml
    Qt5::Quick
    Qt5::WebSockets
)