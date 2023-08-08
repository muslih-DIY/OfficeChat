from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends,Request,APIRouter,Cookie,WebSocket
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlalchemy
from sqlmodel import Session,select
from core.user import (
    UserProfile,User,UserRegisterForm,
    create_user,
    get_user_from_db_id,
    get_user_with_username)
from depends.database import  get_db_Session
from core import config


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_NAME = "authSession"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(session:Session, username: str, password: str)->User:
    try:
        user = get_user_with_username(session,username)
    except sqlalchemy.exc.OperationalError as e:
        return 
    if user and user.password:
        if verify_password(password, user.password):
            return user
        

def create_access_token(username: int, expires_min: int = 60):
    expire = datetime.utcnow() + timedelta(minutes=expires_min or 60)
    to_encode = {"sub":username,"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt,expire

def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=307,headers={'location':'/login'})
    return username
 

async def get_user_from_session_cookie(
        request:Request,
        session = Depends(get_db_Session),
        cookies: str | None = Cookie(default=None,alias=COOKIE_NAME)
        )->UserProfile:
    if cookies:
        try:
            user_id = decode_token(cookies)
            
            userdb = get_user_from_db_id(session,user_id)
            if  userdb.is_active:
                return UserProfile(**userdb.dict())            
        except JWTError :
            raise HTTPException(status_code=302 ,headers={'location':'/login'})        
        
    raise HTTPException(status_code=302,headers={'location':'/login'})


async def get_user_from_session(
        request:Request,
        session = Depends(get_db_Session),
        )->UserProfile:
    
    user_id = request.session.get('id')

    if user_id:
        try:

            userdb = get_user_from_db_id(session,user_id)
            if  userdb.is_active:
                return UserProfile(**userdb.dict())
                        
        except Exception :
            raise HTTPException(status_code=302 ,headers={'location':'/login'})        
        
    raise HTTPException(status_code=302,headers={'location':'/login'})

async def get_user_from_session_for_wb(
        websocket:WebSocket,
        session = Depends(get_db_Session),
        )->UserProfile:
    user_id = websocket.session.get('id')

    if user_id:
        try:

            userdb = get_user_from_db_id(session,user_id)

            if  userdb.is_active:
                return UserProfile(**userdb.dict())
                        
        except Exception :
            raise HTTPException(status_code=302 ,headers={'location':'/login'})        
        
    raise HTTPException(status_code=302,headers={'location':'/login'})



    


router = APIRouter()

@router.post('/newregister')
async def register(
     request:Request,
     newuser:OAuth2PasswordRequestForm = Depends(),
     session:Session = Depends(get_db_Session)       
     ):
    
    newuser.password = get_password_hash(newuser.password)
    session.add(User(**{'password':newuser.password,'name':newuser.username}))
    session.commit()
    return RedirectResponse('/login',status_code=302)

@router.get('/register',response_class=HTMLResponse)
async def registerpage(
     request:Request 
     ):
     context = {'request':request}           
     return config.templates.TemplateResponse('Register.html',context)


@router.get('/login')
async def login(
     request:Request, 
     ):
     context = {'request':request}           
     return config.templates.TemplateResponse('login.html',context)
   



@router.post('/auths',response_class=RedirectResponse)
async def loginAuth(
     request:Request,
     user_form:OAuth2PasswordRequestForm = Depends(),
     session:Session = Depends(get_db_Session)       
     ):
    user = user_form
    redirect = '/login'
    try:

        userdb = authenticate_user(session,user.username,user.password)
    except sqlalchemy.exc.NoResultFound:
        userdb = None
        redirect='/register'

    if not userdb:
        response = RedirectResponse(redirect,status_code=302)
        response.delete_cookie(COOKIE_NAME,httponly=True)
        return response

    response = RedirectResponse('/',status_code=302)

    token,expiry = create_access_token(userdb.name,expires_min=60*8)

    response.set_cookie(COOKIE_NAME,token,max_age=expiry,httponly=True)

    return response


@router.post('/logout',response_class=RedirectResponse)
async def logout(
    request:Request,
    user:UserProfile=Depends(get_user_from_session)
    ):
    request.session.clear()
    response = RedirectResponse('/login',status_code=302)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
        

