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
            #, (Message.from_==person2, Message.to==person1)))

    mesages = session.exec(stmt).all()

    return mesages

def get_unread_chat(session:Session,user:str):
    stmt = select(Message).where(Message.receiver_id==user).where(Message.read==False)
    mesages = session.exec(stmt).all()
    return mesages



def get_users(session:Session,user:str):

    users = session.exec(select(User.name).where(User.name != user)).all()

    return users


# with Session(engine) as session:
#     print(

#     session.exec(
#         select(Message)
#         .where(Message.group_id==None)
#         .where(
#             or_(and_(Message.sender_id==1, Message.receiver_id==1),
#                 and_(Message.sender_id==1, Message.receiver_id==1)))
#         .offset(0)
#         .limit(10)
#         .order_by(-Message.message_id)
#         ).all()
#     )
    