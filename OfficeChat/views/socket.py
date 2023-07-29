from typing import List,Dict
import logging
from fastapi import FastAPI,APIRouter, WebSocket, WebSocketDisconnect,Depends
from fastapi.responses import HTMLResponse
from websockets.exceptions import ConnectionClosed,ConnectionClosedError

from core.user import UserProfile
from core.auth import get_user_from_session,get_user_from_session_for_wb
from chats.manager import ChatProcessor
from model.chat import Message,MessageType,Media
from depends.database import Session,engine

logger = logging.getLogger()

router = APIRouter()




class ChatManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users_live_socket: Dict[str ,List[WebSocket]] = {}
        self.chat_processor = ChatProcessor()

    async def connect(self, websocket: WebSocket,user:str):
        await websocket.accept()
        self.active_connections.append(websocket)

        if user not in self.users_live_socket:
            self.users_live_socket[user] = []
        self.users_live_socket[user].append(websocket)

    def disconnect(self, websocket: WebSocket,user:str):
        self.active_connections.remove(websocket)
        self.users_live_socket[user].remove(websocket)

    async def process_chat(self,msg_data:dict):
        try:

            message:dict = await self.chat_processor(msg=msg_data)
        except :
            logger.error(exc_info=True)
            return
        if not message:
            logger.debug(f'chat processor:{self.chat_processor} returned a ')
            return

        users = {message.get('receiver_id'),message.get('sender_id')}

        for user in users:
            await self.send_personal_message(message,user)
        
    async def broadcast_online_status(self):
        users = self.users_live_socket.keys()
        message = {
                    'type':MessageType.ONLINE_ACK.value,
                    'users':list(users)
                    }

        await self.broadcast(message)

    async def send_personal_message(self, message: dict,user:str):
        websockets:List[WebSocket] = self.users_live_socket.get(user,[])
        for socket in websockets:
            try:
                await socket.send_json(message)

            except ConnectionClosedError:
                self.disconnect(socket,user)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ChatManager()



@router.websocket("/chats/")
async def websocket_endpoint(
    websocket: WebSocket,
    user:UserProfile=Depends(get_user_from_session_for_wb)
    ):
    await manager.connect(websocket,user.id)
    await manager.broadcast_online_status()
    try:

        while True:
            data = await websocket.receive_json(mode='text')
            await manager.process_chat(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket,user.id)
        