import can
import time
import random

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

while True:
    temperature = random.randint(0, 75)

    msg = can.Message(arbitration_id=0x100, data=[temperature,0,0,0,0,0,0,0], is_extended_id=False)

    bus.send(msg)

    print(f"Temperature sent: {temperature} c")

    time.sleep(5)