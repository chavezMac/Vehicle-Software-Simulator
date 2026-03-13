import threading
from can_listener import start_can_listener
from api_server import app

def start_gateway():
    listener_thread = threading.Thread(target=start_can_listener)
    listener_thread.daemon = True
    listener_thread.start()

    print("Starting vehicle API server...")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_gateway()
