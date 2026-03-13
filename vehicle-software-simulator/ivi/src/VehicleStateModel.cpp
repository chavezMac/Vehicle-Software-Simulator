#include "VehicleStateModel.h"
#include <QJsonObject>

VehicleStateModel::VehicleStateModel(QObject *parent) 
    : QObject(parent), m_vehicleSpeed(0.0),m_doorOpen(false),m_temperature(22.0),m_mediaState("STOPPED"){}

double VehicleStateModel::vehicleSpeed() const {
    return m_vehicleSpeed;
}

double VehicleStateModel::temperature() const {
    return m_temperature;
}

bool VehicleStateModel::doorOpen() const {
    return m_doorOpen;
}

QString VehicleStateModel::mediaState() const {
    return m_mediaState;
}

VehicleStateModel::updateFromJson(const QJsonObject &obj) {
    //                                  neccessary check, not guaranteed that the json obj is actually a numeric value
    if (obj.contains("vehicle_speed") && obj["vehicle_speed"].isDouble()) { 
        double newSpeed = obj["vehicle_speed"].toDouble();
        if(!qFuzzyCompare(m_vehicleSpeed,newSpeed)) {
            m_vehicleSpeed = newSpeed;
            emit vehicleSpeedChange();
        }
    }

    if (obj.contains("door_open") && obj["door_open"].isBool()) {
        bool newDoorStatus = obj["door_open"].toBool();
        if(!qFuzzyCompare(m_doorOpen, newDoorStatus)) {
            m_doorOpen = newDoorStatus;
            emit doorOpenChanged();
        }
    }

    if (obj.contains("temperature") && obj["temperature"].isDouble()) {
        double newTemp = obj["temperature"].toDouble();
        if(!qFuzzyCompare(m_temperature, newTemp)) {
            m_temperature = newTemp;
            emit temperatureChanged();
        }
    }

    if(obj.contains("media_state") && obj["media_state"].isString()) {
        QString newMedia = obj["media_state"].toString();
        if(!qFuzzyCompare(m_mediaState, newMedia)) {
            m_mediaState = newMedia;
            emit mediaStateChanged();
        }
    }
}
