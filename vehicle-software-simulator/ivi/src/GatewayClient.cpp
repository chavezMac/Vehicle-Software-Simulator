#include "GatewayClient.h"
#include "VehicleStateModel.h"

#include <QWebSocket>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTimer>
#include <QFile>
#include <QTextStream>
#include <QDateTime>
#include <QIODevice>
#include <QCoreApplication>

GatewayClient::GatewayClient(VehicleStateModel *stateModel, QObject *parent)
    : QObject(parent), m_socket(new QWebSocket), m_stateModel(stateModel), m_reconnectDelayMs(1000){}

void GatewayClient::connectToGateway(const QUrl &url) {
    m_url = url;
    m_socket->open(m_url);
}

void GatewayClient::onConnected() {
    m_reconnectDelayMs = 1000;
    emit connectionStatusChanged(true);
    //optional: send initial message if needed
}

void GatewayClient::onDisconnected() {
    emit connectionStatusChanged(false);
    scheduleReconnect();
}

void GatewayClient::onTextMessageReceived(const QString &message) {
    QJsonDocument doc = QJsonDocument::fromJson(message.toUtf8());
    if(!doc.isObject()) return;
    
    QJsonObject obj = doc.object();
    m_stateModel->updateFromJson(obj);
}

void GatewayClient::onErrorOccurred() {
    QFile f(QCoreApplication::applicationDirPath() + "../logs/ivi_dashboard.log");
    if (f.open(QIODevice::Append | QIODevice::Text)) {
        QTextStream out(&f);
        out << QDateTime::currentDateTime().toString(Qt::ISODate)
            << " WebSocket error: " << m_socket->errorString() << "\n";
    }
    onDisconnected();
}

void GatewayClient::scheduleReconnect() {
    QTimer::singleShot(m_reconnectDelayMs, this, [this]() {
        m_socket->open(m_url);
    });
    m_reconnectDelayMs = qMin(m_reconnectDelayMs * 2, 10000);
}