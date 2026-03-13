import can
from message_decoder import decode_message
from can_logger import log_frame

def start_can_listener():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    print("Gateway listening on CAN bus...")

    for msg in bus:
        log_frame(msg)
        decode_message(msg)
