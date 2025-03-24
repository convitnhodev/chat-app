from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict

class ConnectionManager: 
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_map: Dict[str, WebSocket] = {} 
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if client_id:
            self.connection_map[client_id] = websocket
    
    async def disconnect(self, websocket: WebSocket, client_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if client_id and client_id in self.connection_map:
            del self.connection_map[client_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
async def handle_web_socket_connection(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id} says: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket, client_id)
        await manager.broadcast(f"Client {client_id} left the chat")




    
