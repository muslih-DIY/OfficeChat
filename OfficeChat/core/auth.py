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
from model.user import Userdb,User,UserRegisterForm
from depends.database import  get_db_Session
from core import config

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_NAME = "WrongUser"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(session:Session, username: str, password: str)->Userdb:
    try:
        user = get_user_from_db(session,username)
    except sqlalchemy.exc.OperationalError as e:
        print(e)
        return None
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
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
 

def get_user_from_db(session:Session,username:str):
    
    user  = session.exec(select(Userdb).where(Userdb.name==username)).one()

    return user
def get_user_from_db_id(session:Session,userid:int):
    
    user  = session.get(userid)

    return user

async def get_user_from_session(
        request:Request,
        session = Depends(get_db_Session),
        cookies: str | None = Cookie(default=None,alias=COOKIE_NAME)
        )->User:
    # cookies = request.cookies.get(COOKIE_NAME)
    if cookies:
        try:
            username = decode_token(cookies)
            
            userdb = get_user_from_db(session,username)
            if  userdb.is_active:
                return User(**userdb.dict())            
        except JWTError :
            # raise

            raise HTTPException(status_code=302 ,headers={'location':'/login'})        
    

    raise HTTPException(status_code=302,headers={'location':'/login'})

async def get_wb_user_from_session(
        websocket:WebSocket,
        session = Depends(get_db_Session),
        cookies: str | None = Cookie(default=None,alias=COOKIE_NAME)
        )->User:
    # cookies = request.cookies.get(COOKIE_NAME)
    if cookies:
        try:
            username = decode_token(cookies)
            
            userdb = get_user_from_db(session,username)
            if  userdb.is_active:
                return User(**userdb.dict())            
        except JWTError :
            # raise

            raise HTTPException(status_code=307,headers={'location':'/login'})        
    

    raise HTTPException(status_code=307,headers={'location':'/login'})
    


router = APIRouter()

@router.post('/newregister')
async def register(
     request:Request,
     newuser:OAuth2PasswordRequestForm = Depends(),
     session:Session = Depends(get_db_Session)       
     ):
    
    newuser.password = get_password_hash(newuser.password)
    session.add(Userdb(**{'password':newuser.password,'name':newuser.username}))
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
    
    userdb = authenticate_user(session,user.username,user.password)
    print(userdb)
    if not userdb:
        response = RedirectResponse('/login',status_code=302)
        response.delete_cookie(COOKIE_NAME,httponly=True)
        return response

    response = RedirectResponse('/',status_code=302)

    token,expiry = create_access_token(userdb.name,expires_min=60*8)

    response.set_cookie(COOKIE_NAME,token,max_age=expiry,httponly=True)

    return response

@router.post('/logout',response_class=RedirectResponse)
async def logout(
    user:User=Depends(get_user_from_session),
                ):
    response = RedirectResponse('/login',status_code=302)
    response.delete_cookie(COOKIE_NAME,httponly=True)
    return response
        

