from fastapi import APIRouter,Request,Depends,HTTPException
from fastapi.responses import JSONResponse,HTMLResponse
from sqlmodel import Session,SQLModel,Field
from model.textmesage import TextMsg
from core.auth import get_user_from_session
from core import config
from model.user import User
from depends.database import get_db_Session
from chats.textmessage import store_msg,get_users,get_unread_chat,get_chats_between

router = APIRouter()

class SendTextMsg(SQLModel):
    from_:str = Field(nullable=False)
    to:str = Field(nullable=False)
    content:str = Field(nullable=False)
    group:str  = Field(default='individual')    


@router.post('/send')
async def sendmsg(
    msg:SendTextMsg,
    user:User=Depends(get_user_from_session),
    database:Session = Depends(get_db_Session),
    ):
    if msg.from_ != user.name:
        raise HTTPException(status_code=404 ,detail='Un authorized')
    store_msg(msg)
    return JSONResponse("OK",status_code=200)



@router.get('/',response_class=HTMLResponse)
async def chatpage(
     request:Request,
     user:User=Depends(get_user_from_session) 
     ):
     context = {'request':request,'user':user.name}           
     return config.templates.TemplateResponse('newchatpage.html',context)




@router.get('/users',response_model=list)
async def chatpage(
     request:Request,
     user:User=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     return get_users(database)

@router.get('/get_chat',response_model=list)
async def chatpage(
     request:Request,
     other_person:str,
     offset:int=0,
     user:User=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     return get_chats_between(database,user.name,other_person,offsets=offset)

@router.get('/unread',response_model=list[TextMsg])
async def chatpage(
     request:Request,
     user:User=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     return get_unread_chat(database,user.name)