
from sqlmodel import Session,select,or_,and_,func
from model.chat import Message,Media,MessageType
from core.user import User
from depends.database import engine

def store_msg(session:Session,msg):
    valid_msg = Message(**msg.dict())
    session.add(valid_msg)
    session.commit()
    session.refresh(valid_msg)
    return valid_msg

def get_chats_between(session:Session,person1:int,person2:int,group:str=None,offsets:int=0,limits:int=10):

    stmt = (
        select(Message)
        .where(Message.group_id==group)
        .where(
            or_(and_(Message.sender_id==person1, Message.receiver_id==person2),
                and_(Message.sender_id==person2, Message.receiver_id==person1)))
        .order_by(-Message.message_id)
        .offset(offsets)
        .limit(limits)
        
    )
    mesages = session.exec(stmt).all()
    return mesages

def get_unread_chat(session:Session,user:str):

    stmt = select(Message).where(Message.receiver_id==user).where(Message.read==False)

    mesages = session.exec(stmt).all()
    return mesages

def mark_read(session:Session,user:str,message_ids:list=None):
    print(user,message_ids)
    if not message_ids:message_ids=[]
    stmt = (
        update(TextMsg)
        .where(TextMsg.id.in_(message_ids))
        .where(TextMsg.to==user)
        .values(read=True)
    )
    session.exec(stmt)
    session.commit()
    return True


def get_users(session:Session,user:str):

    users = session.exec(select(User.name).where(User.name != user)).all()

    return users



