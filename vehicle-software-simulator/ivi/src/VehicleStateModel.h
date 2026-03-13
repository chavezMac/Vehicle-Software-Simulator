#pragma once

#include <QObject>

class VehicleStateModel : public QObject {
    Q_OBJECT

    Q_PROPERTY(double vehicleSpeed READ vehicleSpeed NOTIFY vehicleSpeedChanged)
    Q_PROPERTY(bool doorOpen READ doorOpen NOTIFY doorOpenChanged)
    Q_PROPERTY(double temperature READ temperature NOTIFY temperatureChanged)
    Q_PROPERTY(QString mediaState READ mediaState NOTIFY mediaStateChanged)

    public:
        explicit VehicleStateModel(QObject *parent = nullptr);

        double vehicleSpeed() const;
        bool doorOpen() const;
        double temperature() const;
        QString mediaState() const;

    public slots:
        //Called when new snapshot is received from the gateway
        void updateFromJson(const QJsonObject &obj);
    
    signals:
        void vehicleSpeedChanged();
        void doorOpenChanged();
        void temperatureChanged();
        void mediaStateChanged();
    
    private:
        double m_vehicleSpeed;
        bool m_doorOpen;
        double m_temperature;
        QString m_mediaState;
};