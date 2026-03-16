#include <QGuiApplication>
#include <QCommandLineOption>
#include <QCommandLineParser>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QUrl>
#include <QDebug>

#include "VehicleStateModel.h"
#include "GatewayClient.h"

int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);
    QCoreApplication::setApplicationName(QStringLiteral("ivi_dashboard"));
    QCoreApplication::setApplicationVersion(QStringLiteral("1.0"));

    QCommandLineParser parser;
    parser.setApplicationDescription(QStringLiteral("Vehicle IVI dashboard"));
    parser.addHelpOption();
    parser.addVersionOption();

    QCommandLineOption gatewayUrlOption(
        QStringList() << QStringLiteral("g") << QStringLiteral("gateway-url"),
        QStringLiteral("Gateway WebSocket URL (e.g. ws://127.0.0.1:5001)."),
        QStringLiteral("url"));
    parser.addOption(gatewayUrlOption);
    parser.process(app);

    VehicleStateModel vehicleState;
    GatewayClient gateway(&vehicleState);

    QString gatewayUrl = parser.value(gatewayUrlOption).trimmed();
    if (gatewayUrl.isEmpty()) {
        gatewayUrl = qEnvironmentVariable("IVI_GATEWAY_URL").trimmed();
    }
    if (gatewayUrl.isEmpty()) {
        gatewayUrl = QStringLiteral("ws://127.0.0.1:5001");
    }

    QUrl url(gatewayUrl);
    const bool hasValidScheme = (url.scheme() == QStringLiteral("ws") || url.scheme() == QStringLiteral("wss"));
    if (!url.isValid() || !hasValidScheme || url.host().isEmpty()) {
        qCritical() << "Invalid gateway URL:" << gatewayUrl
                    << "(expected ws://host:port or wss://host:port)";
        return -1;
    }

    qInfo() << "Connecting to gateway:" << url.toString();
    gateway.connectToGateway(url);

    QQmlApplicationEngine engine;
    
    //exposes state object to QML as context property
    engine.rootContext()->setContextProperty(QStringLiteral("vehicleState"), &vehicleState);

    //expose connection status
    engine.rootContext()->setContextProperty(QStringLiteral("gatewayClient"), &gateway);

    engine.load(QUrl(QStringLiteral("qrc:/qml/MainView.qml")));
    if (engine.rootObjects().isEmpty()) return -1;

    return app.exec();
}