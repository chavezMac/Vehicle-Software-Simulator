import can
import time
import random

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

print("Door ECU started...")

while True:
    door_open = random.choice([True, False])

    msg = can.Message(arbitration_id=0x200, data=[door_open,0,0,0,0,0,0,0], is_extended_id=False)

    bus.send(msg)

    state = "OPEN" if door_open else "CLOSED"
    print(f"Door state: {state}")

    time.sleep(2)