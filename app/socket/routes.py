from fastapi import APIRouter, WebSocket
from app.socket.handler_websocket import handle_web_socket_connection

ws_router = APIRouter()


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_web_socket_connection(websocket, None)

@ws_router.get("/ws/{client_id}")
async def websocket_endpoint_with_client_id(websocket: WebSocket, client_id: str):
    await handle_web_socket_connection(websocket, client_id)



