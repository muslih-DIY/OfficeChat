from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from enum import Enum,auto

class UserProfile(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    username:str
    email:str = Field(unique=True)
    profile_picture:str
    created_on:int =Field(default_factory=lambda : datetime.now().timestamp())

class User(UserProfile,table=True):
     password:str
     is_active:bool = Field(default=True)

class Group(SQLModel, table=True):
    group_id: int = Field(primary_key=True, index=True)
    group_name: str
    admin_id: int = Field(foreign_key="user.id")


class GroupMember(SQLModel, table=True):
    member_id: int = Field(primary_key=True, index=True)
    group_id: int = Field(foreign_key="group.group_id")
    user_id: int = Field(foreign_key="user.id")

class MessageType(Enum):
    TEXT:int = 1
    MEDIA:int = 2
    READ_ACK = auto()
    ONLINE_ACK = auto()

class Message(SQLModel, table=True):
    message_id: Optional[int] = Field(default=None, primary_key=True, index=True,)
    group_id: int = Field(default=None, index=True)
    sender_id: int = Field(foreign_key="user.id")
    receiver_id: int = Field(default=None, foreign_key="user.id")
    content: str
    type:int = Field(default=MessageType.TEXT.value)
    timestamp: float = Field(default_factory=lambda : datetime.now().timestamp())
    read:bool = Field(default=False)

class Media(SQLModel, table=True):
    media_id: int = Field(primary_key=True, index=True)
    message_id: int = Field(foreign_key="message.message_id")
    media_type: str
    file_path: str

