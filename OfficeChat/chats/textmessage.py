from sqlmodel import Session,select,or_,and_
from model.textmesage import TextMsg
from depends.database import engine

def store_msg(session:Session,msg):
    valid_msg = TextMsg(**msg.dict())
    session.add(valid_msg)
    session.commit()
    session.refresh(valid_msg)
    return valid_msg

def get_chats_between(session:Session,person1:str,person2:str,group:str='individual'):

    stmt = select(TextMsg).where(TextMsg.group==group).where(or_(and_(TextMsg.from_==person1, TextMsg.to==person2),and_(TextMsg.from_==person2, TextMsg.to==person1)))#, (TextMsg.from_==person2, TextMsg.to==person1)))
    
    mesages = session.exec(stmt).all()

    return mesages


# with Session(engine) as session:
#     print(get_chats_between(session,'admin','admin'))