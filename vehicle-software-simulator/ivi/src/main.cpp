#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QUrl>

#include "VehicleStateModel.h"
#include "GatewayClient.h"

int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);

    VehicleStateModel vehicleState;
    GatewayClient gateway(&vehicleState);

    QUrl url(QStringLiteral("ws://10.0.0.44:5001"));
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