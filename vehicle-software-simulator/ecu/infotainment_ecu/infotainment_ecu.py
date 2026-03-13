import can
import time
import random


bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

print("Infotainment ECU started...")

media_states = [(0, "STOPPED"), (1, "PLAYING"), (2, "PAUSED")]

while True:
    state = random.choice(media_states)

    msg = can.Message(arbitration_id=0x300, data=[state[0],0,0,0,0,0,0,0], is_extended_id=False)

    bus.send(msg)

    print(f"Media state: {state[1]}")

    time.sleep(3)