from typing import List
from fastapi import APIRouter,Request,Depends,HTTPException
from fastapi.responses import JSONResponse,HTMLResponse
from sqlmodel import Session,SQLModel,Field,select
from model.textmesage import TextMsg
from core.auth import get_user_from_session
from core import config
from core.config import TEMPLATE
from core.user import UserProfile,User
from model.chat import Message
from depends.database import get_db_Session
from chats.textmessage import(
     store_msg,get_users,get_unread_chat,get_chats_between,
     mark_read
)

router = APIRouter()



@router.post('/send')
async def sendmsg(
    msg:Message,
    user:UserProfile=Depends(get_user_from_session),
    database:Session = Depends(get_db_Session),
    ):
    if msg.from_ != user.name:
        raise HTTPException(status_code=404 ,detail='Un authorized')
    store_msg(msg)
    return JSONResponse("OK",status_code=200)



@router.get('/',response_class=HTMLResponse)
async def chatpage(
     request:Request,
     user:UserProfile=Depends(get_user_from_session) 
     ):
     context = {'request':request,'user_id':user.id,'user':user.name}           
     # response =  config.templates.TemplateResponse('/chatpage_vuejs.html',context)
     with open(TEMPLATE / 'chatpage_vuejs.html', "r") as file:
          response =  HTMLResponse(file.read())
          response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
          response.headers["Pragma"] = "no-cache"
          response.headers["Expires"] = "0"
          return response



@router.get('/me',response_class=JSONResponse)
async def chatpage(
     request:Request,
     user:UserProfile=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     
     return user

@router.get('/contacts',response_class=JSONResponse)
async def chatpage(
     request:Request,
     user:UserProfile=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     
     users =   database.exec(
               f"""with  msg_count as (
               SELECT message.sender_id, count(*) AS msg_counts, max(message.message_id) AS max_1d 
               FROM message
               WHERE message.receiver_id ={user.id}  AND message.read = false GROUP BY message.sender_id
               )

               select u.*,mc.sender_id	,mc.msg_counts from user u LEFT OUTER join msg_count mc on u.id=mc.sender_id
               """
        ).all()
     
     return [
                {
                    'id': user[0],
                    'name': user[1],
                    'message': '',
                    'time': '',
                    'notificationCount': user[9],
                    'avatarSrc': user[4],
                    'online': False
               }
               for user in users
               ] 


@router.get('/get_chat',response_model=list)
async def chatpage(
     request:Request,
     other_person:str,
     offset:int=0,
     user:UserProfile=Depends(get_user_from_session),
     database:Session = Depends(get_db_Session), 
     ):          
     return get_chats_between(database,user.id,other_person,offsets=offset)


