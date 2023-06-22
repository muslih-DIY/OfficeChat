from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine




class TextMsg(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    from_:str = Field(nullable=False)
    to:str = Field(nullable=False)
    content:str = Field(nullable=False)
    group:str  = Field()    
    at:datetime = Field(default_factory=datetime.now)
    read:bool = Field(default=False)


   



