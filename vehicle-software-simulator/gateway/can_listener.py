import can
from message_decoder import decode_message

def start_can_listener():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    print("Gateway listening on CAN bus...")

    for msg in bus:
        decode_message(msg)
