from typing import Optional
from datetime import datetime
import sqlalchemy
from sqlmodel import Field, SQLModel, create_engine,select,Session
from fastapi import Form
from model.chat import User,UserProfile



class UserRegisterForm:
     username :str = Form()
     password:str = Form()


def create_user(session:Session,username,name,password='',email='',profile_picture='')->User|None:
    user = User(**{
        'username':username,
        'name':name,
        'password':password,
        'email':email,
        'profile_picture':profile_picture
        })
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_with_email_id(session,email)->User|None:
    try:
        user  = session.exec(select(User).where(User.email==email)).one()
    
    except sqlalchemy.exc.OperationalError:
        return None
    except sqlalchemy.exc.NoResultFound:
        return None

    return user

def get_user_with_username(session,username)->User|None:
    try:
        user  = session.exec(select(User).where(User.username==username)).one()
    
    except sqlalchemy.exc.OperationalError:
        return None
    except sqlalchemy.exc.NoResultFound:
        return None

    return user

def get_user_from_db_id(session:Session,userid:int):
    
    user  = session.exec(select(User).where(User.id==userid)).one()

    return user
