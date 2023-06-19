from typing import List,Dict
from fastapi import FastAPI,APIRouter, WebSocket, WebSocketDisconnect,Depends
from fastapi.responses import HTMLResponse
from websockets.exceptions import ConnectionClosed,ConnectionClosedError
from model.user import User
from core.auth import get_user_from_session,get_wb_user_from_session
from chats.textmessage import store_msg,TextMsg
from apis.textmessage import SendTextMsg
from depends.database import Session,engine

router = APIRouter()




class ChatManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users_live_socket: Dict[str ,List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket,user:str):
        await websocket.accept()
        self.active_connections.append(websocket)

        if user not in self.users_live_socket:
            self.users_live_socket[user] = []
        self.users_live_socket[user].append(websocket)

    def disconnect(self, websocket: WebSocket,user:str):
        self.active_connections.remove(websocket)
        self.users_live_socket[user].remove(websocket)

    async def process_chat(self,msg):
        users = [msg.from_]
        if not msg.from_==msg.to:
            users.append(msg.to)

        with Session(engine) as session:
            message:TextMsg = store_msg(session=session,msg=msg)

        message.at = message.at.timestamp()
        for user in users:
            await self.send_personal_message(message.dict(),user)
        


    async def send_personal_message(self, message: dict,user:str):
        websockets:List[WebSocket] = self.users_live_socket.get(user,[])
        for socket in websockets:
            try:
                await socket.send_json(message)

            except ConnectionClosedError:
                self.disconnect(socket,user)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ChatManager()



@router.websocket("/chats/")
async def websocket_endpoint(
    websocket: WebSocket,
    user:User=Depends(get_wb_user_from_session)
    ):
    await manager.connect(websocket,user.name)
    try:
        while True:
            data = await websocket.receive_json(mode='text')
            await manager.process_chat(SendTextMsg(**data))
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{user} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket,user.name)