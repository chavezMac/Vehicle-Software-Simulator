"""
Raw WebSocket server for real-time dashboard updates.
Broadcasts vehicle state snapshot when CAN decoder updates state.
"""

import asyncio
import json
import threading
import time
import websockets

from vehicle_state import vehicle_state

WS_PORT = 5001
_clients = set()
_loop = None


def _snapshot():
    """Build JSON-serializable state snapshot."""
    return {
        "vehicle_speed": vehicle_state.vehicle_speed,
        "door_open": vehicle_state.door_open,
        "temperature": vehicle_state.temperature,
        "media_state": vehicle_state.media_state,
        "updated_at": time.time(),
    }


async def _broadcast():
    """Send current state to all connected clients."""
    if not _clients:
        return
    payload = json.dumps(_snapshot())
    dead = set()
    for ws in _clients:
        try:
            await ws.send(payload)
        except Exception:
            dead.add(ws)
    for ws in dead:
        _clients.discard(ws)


def request_broadcast():
    """Called from CAN decoder thread: schedule a broadcast on the WS loop."""
    if _loop is None:
        return
    try:
        asyncio.run_coroutine_threadsafe(_broadcast(), _loop)
    except Exception:
        pass


async def _handler(websocket):
    """Handle one client: register, send initial state, keep connection open."""
    _clients.add(websocket)
    try:
        await websocket.send(json.dumps(_snapshot()))
        async for _ in websocket:
            pass
    finally:
        _clients.discard(websocket)


def _run_loop(loop):
    global _loop
    _loop = loop
    if websockets is None:
        print("WebSocket server skipped (pip install websockets)")
        return
    async def serve():
        async with websockets.serve(_handler, "0.0.0.0", WS_PORT, ping_interval=20, ping_timeout=10):
            await asyncio.Future()
    loop.run_until_complete(serve())


def start_ws_server():
    """Start WebSocket server in a daemon thread. Call once from gateway."""
    if websockets is None:
        return
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=_run_loop, args=(loop,), daemon=True)
    t.start()
    print(f"WebSocket server on 0.0.0.0:{WS_PORT}")
