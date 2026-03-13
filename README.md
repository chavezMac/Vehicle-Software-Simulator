# Vehicle Software Integration Simulator

**A Vehicle Software Integration Simulator built on Raspberry Pi, used to simulate distributed automotive systems. This project includes ECU simulators, a CAN bus network, a gateway service, and a REST API to expose vehicle state. Designed to mimic real-world vehicle software architecture for edutcational, testing, and prototyping purposes.**

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

This project simulates a **distributed automotive software system** on a Raspberry Pi. It is designed to mimic real-world vehicle software architecture, including:  

- Multiple ECU simulators (e.g., speed, door, climate)  
- A CAN bus network using **SocketCAN**  
- A Vehicle Gateway Service aggregating CAN messages  
- A REST API exposing vehicle state for dashboards or apps  

This simulator is ideal for learning **embedded automotive software**, **vehicle network protocols**, and **integration/testing of distributed vehicle systems**.

---

## Architecture

```
ECU simulators
      │
      │ CAN messages
      ▼
Vehicle Gateway Service
      │
      ▼
REST API
      │
      ▼
Dashboard / Apps
```

**Key Components:**

- **ECU Simulators:** Individual processes sending CAN frames.  
- **CAN Bus (SocketCAN):** Simulated vehicle communication network.  
- **Vehicle Gateway:** Decodes CAN messages, maintains vehicle state.  
- **API Server:** Exposes endpoints to read vehicle data.  
- **Dashboard (optional):** Visualizes vehicle state in real time.  

---

## Features

- Simulated vehicle speed, door status, and cabin climate ECUs  
- Virtual CAN bus for communication  
- Real-time message decoding and vehicle state aggregation  
- REST API endpoints for vehicle state consumption  
- Modular structure for easy addition of new ECUs or signals  
- Designed for Raspberry Pi 4/5 or other Linux-based SBCs  

---

## Requirements

- Raspberry Pi 5 (or compatible Linux system)  
- Raspberry Pi OS (64-bit recommended)  
- Python 3.9+  
- Virtual Environment (venv recommended)  

Python packages:

- `python-can`  
- `Flask`  
- `pytest` (for testing)  

Optional hardware for physical CAN:

- PiCAN2 CAN Bus Board or equivalent  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/vehicle-software-simulator.git
cd vehicle-software-simulator
```

2. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up a virtual CAN interface:

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

---

## Usage

1. Run an ECU simulator (e.g., speed ECU):

```bash
python ecu/speed_ecu/speed_ecu.py
```

2. Start the Vehicle Gateway Service:

```bash
python gateway/vehicle_gateway.py
```

3. Query vehicle state via API:

```bash
curl http://localhost:5000/vehicle/speed
curl http://localhost:5000/vehicle/doors
curl http://localhost:5000/vehicle/climate
```

You should see real-time updates reflecting simulated ECU messages.

---

## Project Structure

```
vehicle-software-simulator/
│
├── ecu/                # ECU simulator processes
├── gateway/            # Gateway service and API
├── dashboard/          # Optional front-end dashboard
├── testing/            # Unit and integration tests
├── docs/               # Project documentation
├── configs/            # CAN IDs and vehicle configs
├── scripts/            # Startup and setup scripts
├── venv/               # Python virtual environment
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Testing

Unit and integration tests are located in the `testing/` directory.  

Run tests inside the virtual environment:

```bash
pytest testing/
```

---

## Future Work

- Add additional ECU simulators (e.g., ADAS, infotainment)  
- Simulate OTA updates for ECUs  
- Add real-time dashboard visualization  
- Integrate with Android Automotive OS apps  
- Add vehicle network security features  

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

