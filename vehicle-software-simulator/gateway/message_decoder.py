from vehicle_state import vehicle_state
from signal_database import SignalDatabase

signal_db = SignalDatabase("../configs/signals.json")

def decode_message(msg):
    signal_name, signal_value = signal_db.decode(msg)

    if signal_name:
        setattr(vehicle_state, signal_name.lower(), signal_value)
        try:
            from ws_server import request_broadcast
            request_broadcast()
        except Exception:
            pass
