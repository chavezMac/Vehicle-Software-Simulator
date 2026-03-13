"""
CAN frame logger: writes each received frame to ASC-like text log and JSONL mirror.
Vector CANalyzer/CANoe-style human-readable log plus structured JSON Lines for tooling.
"""

import json
import os
import time

# Log directory: vehicle-software-simulator/logs/
_LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
_ASC_PATH = os.path.join(_LOGS_DIR, "vehicle_can.log")
_JSONL_PATH = os.path.join(_LOGS_DIR, "vehicle_can.jsonl")

_asc_file = None
_jsonl_file = None


def _ensure_logs_open():
    """Create logs directory and open log files on first use."""
    global _asc_file, _jsonl_file
    if _asc_file is not None:
        return
    os.makedirs(_LOGS_DIR, exist_ok=True)
    _asc_file = open(_ASC_PATH, "a", encoding="utf-8")
    _jsonl_file = open(_JSONL_PATH, "a", encoding="utf-8")


def _timestamp(msg):
    """Epoch seconds; use message timestamp if set and valid, else current time."""
    t = getattr(msg, "timestamp", None)
    if t is not None and isinstance(t, (int, float)):
        return float(t)
    return time.time()


def _channel(msg):
    """Channel name; default vcan0 when not set."""
    ch = getattr(msg, "channel", None)
    if ch is not None:
        return str(ch)
    return "vcan0"


def _data_hex(msg):
    """Payload as space-separated hex bytes (e.g. '01 02 FF')."""
    data = getattr(msg, "data", None) or b""
    return " ".join(f"{b:02X}" for b in data)


def log_frame(msg):
    """
    Write one CAN frame to logs/vehicle_can.log (ASC-like) and logs/vehicle_can.jsonl.
    Swallows exceptions so logger failure cannot crash the gateway loop.
    """
    try:
        _ensure_logs_open()
        ts = _timestamp(msg)
        ch = _channel(msg)
        direction = "Rx" if getattr(msg, "is_rx", True) else "Tx"
        arb_id = getattr(msg, "arbitration_id", 0)
        dlc = getattr(msg, "dlc", None)
        if dlc is None:
            data = getattr(msg, "data", None) or b""
            dlc = len(data)
        data_hex_str = _data_hex(msg)
        data_bytes = list(getattr(msg, "data", None) or b"")

        # ASC-like: timestamp channel direction id_hex DLC data_hex
        asc_line = f"{ts:.6f}  {ch}  {direction}  {arb_id:X}  {dlc}  {data_hex_str}\n"
        _asc_file.write(asc_line)
        _asc_file.flush()

        # JSONL mirror
        record = {
            "timestamp": ts,
            "channel": ch,
            "direction": direction,
            "arbitration_id_hex": f"{arb_id:X}",
            "arbitration_id_dec": arb_id,
            "dlc": dlc,
            "data_hex": data_hex_str,
            "data_bytes": data_bytes,
        }
        _jsonl_file.write(json.dumps(record) + "\n")
        _jsonl_file.flush()
    except Exception:
        # Do not let logger crash the CAN listener
        pass
