import websockets
import json
import time
import asyncio

from typing import Any, Dict, List

async def _collect_ws_snapshots_async(
    url: str, duration_sec: float, 
    min_messages: int, recv_timeout_sec: float = 1.0) -> List[Dict[str, Any]]:
    """
    Connect to WebSocket, collect JSON snapshots until duration expires.
    Returns : [{"ts_recv": monotonic_time, "payload": decoded_json}, ...]
    """

    results: List[Dict[str, Any]] = []
    deadline = time.monotonic() + duration_sec

    async with websockets.connect(url) as ws:
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            timeout = min(recv_timeout_sec, max(0.01, remaining))

            try:
                raw =  await asyncio.wait_for(ws.recv(), timeout=timeout)
                ts_recv = time.monotonic()
            except asyncio.TimeoutError:
                continue
            except websockets.ConnectionClosed:
                break
            
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                continue

            results.append({"ts_recv": ts_recv, "payload": payload})
    
    if len(results) < min_messages:
        raise AssertionError(
            f"Insufficient messages received: {len(results)} < {min_messages}"
        )
    
    return results

def collect_ws_snapshots(
    url: str,
    duration_sec: float,
    min_messages: int,
    recv_timeout_sec: float = 1.0,
) -> List[Dict[str, Any]]:
    """
    Sync wrapper for tests
    """
    return asyncio.run(_collect_ws_snapshots_async(
        url = url, duration_sec = duration_sec, 
        min_messages = min_messages, recv_timeout_sec = recv_timeout_sec))