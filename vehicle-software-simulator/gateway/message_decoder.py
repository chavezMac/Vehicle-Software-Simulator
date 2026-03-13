from vehicle_state import vehicle_state

def decode_message(msg):

    if msg.arbitration_id == 0x130:
        vehicle_state.speed = msg.data[0]
    elif msg.arbitration_id == 0x200:
        vehicle_state.door_open = bool(msg.data[0])
    elif msg.arbitration_id == 0x300:
        vehicle_state.temperature = msg.data[0]
