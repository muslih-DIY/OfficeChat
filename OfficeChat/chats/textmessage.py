from sqlmodel import Session,select,or_,and_,func,update
from model.textmesage import TextMsg
from model.user import Userdb
from depends.database import engine

def store_msg(session:Session,msg):
    valid_msg = TextMsg(**msg.dict())
    session.add(valid_msg)
    session.commit()
    session.refresh(valid_msg)
    return valid_msg

def get_chats_between(session:Session,person1:str,person2:str,group:str='individual',offsets:int=0,limits:int=10):

    stmt = (
        select(TextMsg)
        .where(TextMsg.group==group)
        .where(
            or_(and_(TextMsg.from_==person1, TextMsg.to==person2),
                and_(TextMsg.from_==person2, TextMsg.to==person1)))
        .offset(offsets)
        .limit(limits)
        .order_by(-TextMsg.id)
    )
    mesages = session.exec(stmt).all()

    return mesages

def get_unread_chat(session:Session,user:str):
    stmt = (
        select(TextMsg.from_,func.count(TextMsg.id))
        .where(TextMsg.to==user)
        .where(TextMsg.read==False)
        .group_by(TextMsg.from_)
    )
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

    users = session.exec(select(Userdb.name).where(Userdb.name != user)).all()

    return users

# with Session(engine) as session:

#     print(get_chats_between(session,'admin','muslih'))

