from enum import auto
import logging
from typing import Any
from sqlmodel import Session,select
from model.chat import MessageType as MType,Message
from depends.database import Session,engine


logger = logging.getLogger()



def get_msg(session:Session,message_id:int):

    return session.exec(select(Message).where(Message.message_id==message_id)).one()

def store_msg(session:Session,msg:Message):
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg




class ChatProcessor:
    async def __call__(self,msg:dict) -> Any:

        chat_type = msg.get('type')
        if not chat_type:
            logging.debug(f"recieved a chat without type from {msg.get('sender_id')} to {msg.get('receiver_id')}")
            return 0
        
        mtype = MType(chat_type)

        if not mtype:
            logging.debug(f"recieved a chat with invalid type from {msg.get('sender_id')} to {msg.get('receiver_id')}")
            return 0
        print(mtype)
        processor  =  getattr(self,mtype.name.lower())
        print(processor)
        response = await processor(msg)
        return response
    
    async def text(self,msg_data:dict):

        msg = Message(**msg_data)
        msg.read = True if msg.sender_id==msg.receiver_id else False 

        with Session(engine) as session:
            message:Message = store_msg(session=session,msg=msg)
                
        return message.dict()

    async def read_ack(self,msg_data:dict):

        message_id = msg_data.get('message_id')
        if not message_id:
            logging.debug(f"recieved a read acknowledge without message_id")
            return 0
        with Session(engine) as session:
            message:Message = get_msg(session=session,message_id=message_id)
            message.read = True
            message = store_msg(session=session,msg=message)
            message.type=3
        return message.dict()



