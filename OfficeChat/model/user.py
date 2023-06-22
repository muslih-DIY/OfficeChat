from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
from fastapi import Form


class User(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
   

class Userdb(User,table=True):
     password:str
     is_active:bool = Field(default=True)


# class UserRegister(SQLModel):
#      name: str = Field(unique=True)
#      password:str

class UserRegisterForm:
     username :str = Form()
     password:str = Form()