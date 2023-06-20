from sqlmodel import Session,select,or_,and_
from model.textmesage import TextMsg
from model.user import Userdb
from depends.database import engine

def store_msg(session:Session,msg):
    valid_msg = TextMsg(**msg.dict())
    session.add(valid_msg)
    session.commit()
    session.refresh(valid_msg)
    return valid_msg

def get_chats_between(session:Session,person1:str,person2:str,group:str='individual',offsets:int=0,limits:int=40):

    stmt = (
        select(TextMsg)
        .where(TextMsg.group==group)
        .where(
            or_(and_(TextMsg.from_==person1, TextMsg.to==person2),
                and_(TextMsg.from_==person2, TextMsg.to==person1)))
        .offset(offsets)
        .limit(limits)
    )
            #, (TextMsg.from_==person2, TextMsg.to==person1)))
    
    mesages = session.exec(stmt).all()

    return mesages

def get_unread_chat(session:Session,user:str):
    stmt = select(TextMsg).where(TextMsg.to==user).where(TextMsg.read==False)
    mesages = session.exec(stmt).all()
    return mesages


def get_users(session:Session):

    users = session.exec(select(Userdb.name)).all()

    return users

# with Session(engine) as session:

#     print(get_unread_chat(session,'admin'))