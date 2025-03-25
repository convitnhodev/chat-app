from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Optional
from app.socket.auth import authenticate_websocket

class ConnectionManager: 
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_info: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None) -> Optional[str]:
        try: 
            # First accept the connection
            await websocket.accept()
            print("WebSocket connection accepted")  # Debug log

            # Then authenticate
            is_authenticated, user_data = await authenticate_websocket(websocket)
            if not is_authenticated or not user_data:
                print("Authentication failed")  # Debug log
                return None
            
            # Use username from token as connection_id if no client_id provided
            connection_id = client_id or user_data.get('sub')
            if not connection_id:
                print("No valid connection ID")  # Debug log
                return None

            self.active_connections[connection_id] = websocket
            self.user_info[connection_id] = user_data
            
            print(f"User {connection_id} connected successfully")  # Debug log
            return connection_id
           
        except Exception as e:
            print(f"Connection error: {str(e)}")  # Debug log
            return None
    
    async def disconnect(self, connection_id: str):
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            try:
                await websocket.close()
            except:
                pass  # Connection might already be closed
            self.active_connections.pop(connection_id, None)
            self.user_info.pop(connection_id, None)
            print(f"User {connection_id} disconnected")  # Debug log

    async def send_personal_message(self, message: str, connection_id: str):
        if websocket := self.active_connections.get(connection_id):
            try:
                await websocket.send_text(message)
            except Exception as e:
                print(f"Error sending personal message: {str(e)}")  # Debug log
                await self.disconnect(connection_id)

    async def broadcast(self, message: str, exclude: Optional[str] = None):
        disconnected = []
        for conn_id, websocket in self.active_connections.items():
            if conn_id != exclude:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    print(f"Error broadcasting to {conn_id}: {str(e)}")  # Debug log
                    disconnected.append(conn_id)
        
        # Clean up disconnected clients
        for conn_id in disconnected:
            await self.disconnect(conn_id)

manager = ConnectionManager()

async def handle_websocket_connection(websocket: WebSocket, client_id: Optional[str] = None):
    connection_id = await manager.connect(websocket, client_id)
    if not connection_id:
        return
    
    try:
        user_info = manager.user_info.get(connection_id, {})
        username = user_info.get('sub', connection_id)
        
        await manager.broadcast(f"User {username} joined")
        print(f"User {username} joined chat")  # Debug log
        
        while True:
            try:
                data = await websocket.receive_text()
                print(f"Received message from {username}: {data}")  # Debug log
                await manager.send_personal_message(f"You sent: {data}", connection_id)
                await manager.broadcast(f"User {username}: {data}", connection_id)
            except WebSocketDisconnect:
                print(f"WebSocket disconnected for {username}")  # Debug log
                break
            except Exception as e:
                print(f"Error handling message: {str(e)}")  # Debug log
                break
    
    finally:
        await manager.disconnect(connection_id)
        await manager.broadcast(f"User {username} left")




    
