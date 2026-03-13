# Vehicle Software Integration Simulator

A vehicle software simulator on Raspberry Pi that simulates distributed automotive systems: ECU simulators, a CAN bus, a gateway with REST + WebSocket telemetry, a web dashboard, and an optional Qt/QML IVI (infotainment) app. Built for learning, testing, and prototyping vehicle software architecture.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Project Structure](#project-structure)
8. [Testing](#testing)
9. [Future Work](#future-work)
10. [License](#license)

---

## Overview

This project simulates a **distributed automotive software system** on a Raspberry Pi (or other Linux SBC), including:

- **ECU simulators** (speed, door, infotainment, temperature) sending CAN frames
- **SocketCAN** virtual bus (`vcan0`)
- **Vehicle gateway** that decodes CAN, keeps vehicle state, logs frames (ASC-like + JSONL), and exposes REST + WebSocket
- **Web dashboard** (HTML/JS) with real-time updates over WebSocket
- **Qt/QML IVI app** (C++) – optional in-vehicle style HMI that connects to the gateway via WebSocket

---

## Architecture

```
ECU simulators (speed, door, infotainment, temperature)
      │
      │ CAN frames (vcan0)
      ▼
Vehicle Gateway (Python)
      ├── CAN listener + message decoder → vehicle_state
      ├── CAN logger → logs/vehicle_can.log, logs/vehicle_can.jsonl
      ├── REST API (Flask, port 5000)
      └── WebSocket server (port 5001) → real-time snapshots
      │
      ├──────────────────────────────────┬─────────────────────────────┐
      ▼                                  ▼                             ▼
Web Dashboard (HTML/JS)           Qt/QML IVI app                 REST clients
(port 8000, static server)        (C++, local or remote)          (curl, scripts)
```

**Components:**

| Component | Role |
|-----------|------|
| **ECU simulators** | Python processes that send CAN frames on `vcan0` (speed, door, media, climate). |
| **Gateway** | Listens on CAN, decodes via `configs/signals.json`, updates `vehicle_state`, logs to `logs/`, serves REST and WebSocket. |
| **Web dashboard** | Static HTML/JS; connects to gateway WebSocket for live speed, door, media. |
| **IVI app** | C++/Qt/QML app; connects to gateway WebSocket and displays vehicle state in a Tesla-style HMI. |

---

## Features

- Simulated **speed**, **door**, **infotainment**, and **temperature** ECUs
- **CAN logging** – Vector CANalyzer/CANoe–style ASC text + JSONL mirror in `logs/`
- **REST API** – `/vehicle/speed`, `/vehicle/doors`, `/vehicle/climate`, `/vehicle/media`
- **WebSocket telemetry** – JSON snapshots pushed on state change; used by web dashboard and IVI
- **Web dashboard** – real-time UI with reconnect and connection status
- **Qt/QML IVI** – optional C++ dashboard with WebSocket client and QML UI
- **Modular config** – `configs/signals.json` drives CAN decoding; easy to add signals/ECUs

---

## Requirements

- Raspberry Pi 4/5 (or compatible Linux)
- Raspberry Pi OS 64-bit (or similar)
- **Python 3.9+** and a **venv** for gateway, ECUs, and web tooling
- **Qt 5 or 6** (optional, only for building the IVI app)

**Python (gateway/dashboard):**

- `python-can`, `Flask`, `flask-cors`, `websockets` (see `vehicle-software-simulator/requirements.txt`)

**IVI (optional):**

- Qt5: `qtbase5-dev`, `qtdeclarative5-dev`, `libqt5websockets5-dev`, `cmake`, `build-essential`
- Or Qt6 equivalents if available on your distro

**Virtual CAN:**

- `vcan0` (see Installation).

---

## Installation

1. **Clone and enter the app directory:**

```bash
git clone https://github.com/yourusername/Vehicle-Software-Simulator.git
cd Vehicle-Software-Simulator/vehicle-software-simulator
```

2. **Create and activate a Python virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
```

3. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create and bring up the virtual CAN interface:**

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

5. **(Optional) Build the Qt IVI app** (requires Qt dev packages):

```bash
cd ivi
mkdir -p build && cd build
cmake ..    # Use Qt5 or Qt6 per your CMakeLists.txt
make -j$(nproc)
```

---

## Usage

**1. Start the gateway** (required for dashboard and IVI):

```bash
cd vehicle-software-simulator
source .venv/bin/activate
cd gateway
python vehicle_gateway.py
```

You should see: WebSocket server on `0.0.0.0:5001`, REST on port 5000, and “Gateway listening on CAN bus…”.

**2. (Optional) Start ECU simulators** (in separate terminals):

```bash
cd vehicle-software-simulator
source .venv/bin/activate
python ecu/speed_ecu/speed_ecu.py
python ecu/door_ecu/door_ecu.py
python ecu/infotainment_ecu/infotainment_ecu.py
python ecu/temperature_ecu/temperature_ecu.py
```

**3. (Optional) Serve the web dashboard:**

```bash
cd vehicle-software-simulator/dashboard
python -m http.server 8000
```

Open `http://<Pi-IP>:8000` in a browser; it connects to the gateway WebSocket at `<Pi-IP>:5001`.

**4. (Optional) Run the Qt IVI app:**

```bash
cd vehicle-software-simulator/ivi/build
./ivi_dashboard
```

Ensure the gateway is running; the IVI connects to `ws://127.0.0.1:5001` (or the URL in `main.cpp`).

**REST examples:**

```bash
curl http://localhost:5000/vehicle/speed
curl http://localhost:5000/vehicle/doors
curl http://localhost:5000/vehicle/climate
curl http://localhost:5000/vehicle/media
```

---

## Project Structure

```
Vehicle-Software-Simulator/
├── README.md
├── LICENSE
└── vehicle-software-simulator/
    ├── configs/
    │   └── signals.json          # CAN ID → signal name, byte, type
    ├── ecu/
    │   ├── speed_ecu/
    │   ├── door_ecu/
    │   ├── infotainment_ecu/
    │   └── temperature_ecu/
    ├── gateway/
    │   ├── vehicle_gateway.py     # Entry: CAN listener + Flask + WebSocket
    │   ├── can_listener.py
    │   ├── can_logger.py         # logs/vehicle_can.log, .jsonl
    │   ├── message_decoder.py
    │   ├── signal_database.py
    │   ├── vehicle_state.py
    │   ├── api_server.py         # REST
    │   └── ws_server.py          # WebSocket telemetry
    ├── dashboard/
    │   └── index.html            # Web dashboard (WebSocket)
    ├── ivi/                      # Qt/QML IVI app (C++)
    │   ├── CMakeLists.txt
    │   ├── src/
    │   │   ├── main.cpp
    │   │   ├── VehicleStateModel.*
    │   │   └── GatewayClient.*
    │   └── qml/
    │       ├── MainView.qml
    │       └── qml.qrc
    ├── logs/                     # Created at runtime
    │   ├── vehicle_can.log       # ASC-like CAN log
    │   └── vehicle_can.jsonl     # JSONL mirror
    ├── requirements.txt
    └── .venv/                    # Python virtual environment
```

---

## Testing

Run tests from the project root with the venv activated:

```bash
cd vehicle-software-simulator
source .venv/bin/activate
pytest testing/
```

(Add tests under `testing/` as needed.)

---

## Future Work

- More ECUs (e.g. ADAS, BMS)
- DBC-based signal definitions (e.g. cantools) alongside or instead of `signals.json`
- IVI: direct SocketCAN client option, full-screen/kiosk mode
- OTA simulation, security/authentication for API and WebSocket

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
