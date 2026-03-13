import json

class SignalDatabase:
    def __init__(self, path):
        
        with open(path) as f:
            self.db = json.load(f)

        self.signals = self.db["signals"]

    def decode(self, msg):
        signal = self.signals.get(str(msg.arbitration_id))

        if not signal:
            return None
        
        raw_value = msg.data[signal["byte"]]

        if signal["type"] == "int":
            return signal["name"], int(raw_value)
        
        if signal["type"] == "bool":
            return signal["name"], bool(raw_value)
        
        if signal["type"] == "enum":
            return signal["name"], signal["values"].get(str(raw_value), "UNKNOWN")
        
        return None