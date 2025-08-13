from broadcaster import Broadcast
from fastapi import WebSocket
from typing import Dict
from .config import settings

BROADCAST_URL = settings.redis_url
broadcaster = Broadcast(BROADCAST_URL)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, post_id: int):
        await websocket.accept()
        if post_id not in self.active_connections:
            self.active_connections[post_id] = []
        self.active_connections[post_id].append(websocket)

    def disconnect(self, websocket: WebSocket, post_id: int):
        if post_id in self.active_connections:
            self.active_connections[post_id].remove(websocket)
            if not self.active_connections[post_id]:
                del self.active_connections[post_id]

    async def broadcast_to_post(self, post_id: int, message: str):
        channel = f"post_{post_id}"
        await broadcaster.publish(channel=channel, message=message)

manager = ConnectionManager()
