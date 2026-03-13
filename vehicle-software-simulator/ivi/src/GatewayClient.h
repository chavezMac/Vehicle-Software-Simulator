#pragma once

#include <QObject>
#include <QUrl>

class QWebSocket;
class VehicleStateModel;

class GatewayClient : public QObject {
    Q_OBJECT

    public:
        explicit GatewayClient(VehicleStateModel *stateModel, QObject *parent = nullptr);

        void connectToGateway(const QUrl &url);

    signals:
        void connectionStatusChanged(bool connected);
    
    private slots:
        void onConnected();
        void onDisconnected();
        void onTextMessageReceived(const QString &message);
        void onErrorOccurred(); //actual signature depends on Qt version
    
    private:
        void scheduleReconnect(); //timer based

        QWebSocket *m_socket;
        VehicleStateModel *m_stateModel;
        QUrl m_url;
        int m_reconnectDelayMs;
};