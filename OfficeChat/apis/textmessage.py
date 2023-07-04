from typing import List
from fastapi import APIRouter,Request,Depends,HTTPException
from fastapi.responses import JSONResponse,HTMLResponse
from sqlmodel import Session,SQLModel,Field
from model.textmesage import TextMsg
from core.auth import get_user_from_session
from core import config
from model.user import User
from depends.database import get_db_Session
from chats.textmessage import(
     store_msg,get_users,get_unread_chat,get_chats_between,
     mark_read
)

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
     response =  config.templates.TemplateResponse('newchatpage.html',context)
     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
     response.headers["Pragma"] = "no-cache"
     response.headers["Expires"] = "0"
     return response




@router.get('/users',response_class=JSONResponse)
async def chatpage(
     request:Request,
     user:User=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     return get_users(database,user.name)

@router.get('/get_chat',response_model=list)
async def chatpage(
     request:Request,
     other_person:str,
     offset:int=0,
     user:User=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     return get_chats_between(database,user.name,other_person,offsets=offset)

@router.get('/unread',response_model=list)
async def chat_unread(
     request:Request,
     user:User=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     return get_unread_chat(database,user.name)

@router.post('/update_read',response_class=JSONResponse)
async def chat_update_read(
     request:Request,
     message_id:List[int],
     user:User=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     if mark_read(database,user.name,message_id):
          return JSONResponse('OK')
     