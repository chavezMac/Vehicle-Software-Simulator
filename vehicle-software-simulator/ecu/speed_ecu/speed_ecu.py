import can
import time
import random

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

while True:
    speed = random.randint(0,120)

    msg = can.Message(arbitration_id=0x130, data=[speed,0,0,0,0,0,0,0], is_extended_id=False)

    bus.send(msg)

    print(f"Speed sent: {speed} km/h")

    time.sleep(1)
