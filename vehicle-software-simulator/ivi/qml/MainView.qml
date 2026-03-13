import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: 1024
    height: 600
    color: "#111"

    Column {
        anchors.centerIn: parent
        spacing: 24

        Text {
            text: "Vehicle Software Simulator"
            color: "white"
            font.pointSize: 28
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Row {
            spacing: 24
            anchors.horizontalCenter: parent.horizontalCenter

            // Speed card
            Rectangle {
                width: 200; height: 160; radius: 12
                color: "#222"
                Column {
                    anchors.centerIn: parent
                    spacing: 8
                    Text { text: "Speed"; color: "white"; font.pointSize: 16 }
                    Text {
                        text: vehicleState.vehicleSpeed.toFixed(0) + " km/h"
                        color: "white"
                        font.pointSize: 32
                    }
                }
            }

            // Door card
            Rectangle {
                width: 200; height: 160; radius: 12
                color: "#222"
                Column {
                    anchors.centerIn: parent
                    spacing: 8
                    Text { text: "Driver Door"; color: "white"; font.pointSize: 16 }
                    Text {
                        text: vehicleState.doorOpen ? "OPEN" : "CLOSED"
                        color: vehicleState.doorOpen ? "#f97373" : "#4ade80"
                        font.pointSize: 32
                    }
                }
            }

            // Media card
            Rectangle {
                width: 200; height: 160; radius: 12
                color: "#222"
                Column {
                    anchors.centerIn: parent
                    spacing: 8
                    Text { text: "Media"; color: "white"; font.pointSize: 16 }
                    Text {
                        text: vehicleState.mediaState
                        color: "white"
                        font.pointSize: 24
                    }
                }
            }

            // Temperature card
            Rectangle {
                width: 200; height: 160; radius 12
                color: "#222"
                Column {
                    anchors.centerIn: parent
                    spacing: 8
                    Text { text: "Temp"; color: "white"; font.pointSize: 16 }
                    Text {
                        text: vehicleState.temperature + " c"
                        color: "white"
                        font.pointSize: 24
                    }
                }
            }

        }

        Text {
            // Hook this to gatewayClient.connectionStatusChanged if desired
            text: "Live"  // or "Disconnected"
            color: "#4ade80"
            font.pointSize: 14
            opacity: 0.8
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}