#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys
import time

import websockets


REQUIRED_KEYS = ("vehicle_speed", "door_open", "media_state", "temperature")
VALID_MEDIA_STATES = {"STOPPED", "PLAYING", "PAUSED"}


def validate_payload(payload):
    for key in REQUIRED_KEYS:
        if key not in payload:
            raise AssertionError(f"Missing key in payload: {key}")

    if not isinstance(payload["vehicle_speed"], (int, float)):
        raise AssertionError("vehicle_speed must be number")
    if not isinstance(payload["door_open"], bool):
        raise AssertionError("door_open must be bool")
    if not isinstance(payload["media_state"], str):
        raise AssertionError("media_state must be string")
    if payload["media_state"] not in VALID_MEDIA_STATES:
        raise AssertionError(
            f"media_state must be one of {sorted(VALID_MEDIA_STATES)}; got {payload['media_state']}"
        )
    if not isinstance(payload["temperature"], (int, float)):
        raise AssertionError("temperature must be number")


async def verify(url, duration_sec, recv_timeout_sec):
    changed = {key: False for key in REQUIRED_KEYS}
    last_seen = {}
    received = 0
    deadline = time.monotonic() + duration_sec

    async with websockets.connect(url) as ws:
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            timeout = min(recv_timeout_sec, max(0.05, remaining))
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
            except asyncio.TimeoutError:
                continue
            except websockets.ConnectionClosed as exc:
                raise AssertionError(f"WebSocket closed before verification finished: {exc}") from exc

            received += 1
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise AssertionError(f"Invalid JSON payload: {raw}") from exc

            validate_payload(payload)

            for key in REQUIRED_KEYS:
                value = payload[key]
                if key in last_seen and last_seen[key] != value:
                    changed[key] = True
                last_seen[key] = value

    never_changed = [k for k, did_change in changed.items() if not did_change]
    if received == 0:
        raise AssertionError("No telemetry messages received")
    if never_changed:
        raise AssertionError(
            "Fields did not change during verification window: " + ", ".join(never_changed)
        )

    return received


def parse_args():
    parser = argparse.ArgumentParser(description="Verify telemetry payload contract and live field changes.")
    parser.add_argument("--url", default="ws://127.0.0.1:5001", help="WebSocket URL")
    parser.add_argument("--duration", type=float, default=20.0, help="Verification window in seconds")
    parser.add_argument(
        "--recv-timeout",
        type=float,
        default=1.0,
        help="Per-receive timeout while collecting messages",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        received = asyncio.run(verify(args.url, args.duration, args.recv_timeout))
    except Exception as exc:
        print(f"[telemetry-verify] FAIL: {exc}")
        return 1

    print(f"[telemetry-verify] PASS: received {received} messages and all required fields changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
