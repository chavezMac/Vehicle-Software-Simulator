import platform
import socket
import time
from urllib.error import URLError
from urllib.request import urlopen

import pytest

from testing.helpers.assertions import assert_changed, assert_has_keys, assert_not_stale
from testing.helpers.process_runner import ProcessGroup
from testing.helpers.ws_probe import collect_ws_snapshots


def wait_until_http_ready(url, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except URLError:
            time.sleep(0.2)
    raise AssertionError(f"HTTP service did not become ready: {url}")


def wait_until_tcp_ready(host, port, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            time.sleep(0.2)
    raise AssertionError(f"TCP service did not become ready: {host}:{port}")


@pytest.mark.skipif(platform.system() != "Linux", reason="SocketCAN golden test requires Linux/vcan0")
def test_golden_demo():
    timeout_total_sec = 20
    required_fields = ["vehicle_speed", "door_open", "media_state", "temperature"]
    procs = ProcessGroup()

    try:
        procs.start_gateway()
        procs.start_ecu("speed")
        procs.start_ecu("door")
        procs.start_ecu("infotainment")
        procs.start_ecu("temperature")

        wait_until_http_ready("http://127.0.0.1:5000/vehicle/speed", timeout=10)
        wait_until_tcp_ready("127.0.0.1", 5001, timeout=10)

        snapshots = collect_ws_snapshots(
            url="ws://127.0.0.1:5001",
            duration_sec=timeout_total_sec,
            min_messages=10,
        )

        for snap in snapshots:
            assert_has_keys(snap, required_fields)

        assert_changed(snapshots, "vehicle_speed")
        assert_changed(snapshots, "door_open")
        assert_changed(snapshots, "media_state")
        assert_changed(snapshots, "temperature")

        assert_not_stale(snapshots, field="vehicle_speed", max_stale_sec=10)
        assert_not_stale(snapshots, field="door_open", max_stale_sec=10)
        assert_not_stale(snapshots, field="media_state", max_stale_sec=10)
        assert_not_stale(snapshots, field="temperature", max_stale_sec=10)
    finally:
        procs.stop_all()

