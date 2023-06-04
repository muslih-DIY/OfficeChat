from typing import Dict, Optional
import  random
from datetime import timedelta,datetime
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials 
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,HTTP_307_TEMPORARY_REDIRECT
from fastapi import Request,Depends,APIRouter,Header
from fastapi.responses import HTMLResponse,Response
from abc import ABC,abstractmethod
from enum import Enum

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
SESSION_EXPIRE_MINUTES = 15
ACCESS_TOKEN_EXPIRE_MINUTES = 10

class KeyType(Enum):
    SESSION = 3
    ACCESS = 4



class AuthData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str
    expiry:float

class Tokendb(Token):
    username:str
    session:str # token from cookies/refresh token

class SCookies(BaseModel):
    cookies:str
    expiry:float

class SCookiesDB(SCookies):
    username:str

class User(BaseModel):
    username: str
    email: str = None
    full_name: str  = None
    disabled: bool = None


class UserInDB(User):
    hashed_password: str



router = APIRouter()

autherization = HTTPBearer(auto_error=False)

class LoginManager(ABC):
    """This is a abstrat class impliment the login by header or session.

      The concrete class impliment how:
      
          -  how user details get for autherisation in `get_user` abstract method

          -  The saving of cookies (may be in redis/database/dictionary/in-memmorycache ) in `save_cookies`

    """
    def __init__(self, tokenUrl: str, scheme_name: str | None = None, scopes: Dict[str, str] | None = None, description: str | None = None, auto_error: bool = True):
        
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        self.login_page = '/login'
        self.session_cookey = 'Authkey'


    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self,password):
        return self.pwd_context.hash(password)
    
    
    @abstractmethod
    def get_user(self,user_id:str)-> User:
        "get information of user from other cached/fast source to use in every session"
        pass

    @abstractmethod
    def get_userdb(self,user_id:str)-> UserInDB:
        "Return the latest information of user from db"
        pass


    @abstractmethod
    def get_cookies(user:str):
        'return cooies details against a user'

    @abstractmethod
    def get_token(user:str):
        'return token against the user'

    @abstractmethod
    def save_cookies(cookies:SCookiesDB):
        pass

    @abstractmethod
    def save_token(cookies:Tokendb):
        pass

    @abstractmethod
    def get_token_against_cookie(cookies:str):
        'return token against a cookie' 
        pass

    @abstractmethod
    def invalidate_cookie(cookies:str):
        """
        remove cookie from storage and invalidate a session
        remove all the token against the cookies

        """
        pass


    def authenticate_user(self,username: str, password: str):
        user = self.get_userdb(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
    
        
    def create_access_token(self,user,scopes, expires_min: int = None):
        data={
            "sub": user.username,
            "type":KeyType.ACCESS.value,
            "scopes": scopes
            }
        return self.generate_token(data,expires_min)
    
    def create_session_token(self,user,scopes, expires_min: int = None):
        data={
            "sub": user.username,
            "type":KeyType.SESSION.value,
            "scopes": scopes
            }
        return self.generate_token(data,expires_min)
    
    def generate_token(self,data,expires_min: int = None):

        expires_delta = timedelta(
            minutes=expires_min or ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire,"rand":random.randrange(10,50)})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt,expire
    
    def decode_jwt(self,token):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        scops: str = payload.get("scopes")
        type = payload.get("type")
        return (type,username,scops)
    

    async def get_user_from_auth(
            self,
            Authkey:HTTPAuthorizationCredentials =Depends(autherization)
            ):
        print(Authkey)
        if Authkey is not None:
            try:

                ttype,username,scops = self.decode_jwt(Authkey.credentials)


            except (JWTError, ValidationError):
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                        )
            print(ttype)            
            if ttype and ttype==KeyType.ACCESS.value:              
                if username:
                    user = self.get_user(username)
                    if user and not user.disabled:
                        return user
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
                )    


    async def get_user_from_cookie(
            self,
            request: Request
            ) -> Optional[dict]:
        Authkey = request.cookies.get(self.session_cookey)
        if Authkey is not None:
            try:

                type,username,scops = self.decode_jwt(Authkey)
            except (JWTError, ValidationError):
                #create a dummy response and delete the key  and return the header
                response = Response()
                response.delete_cookie(self.session_cookey)
                raise HTTPException(
                    status_code=HTTP_307_TEMPORARY_REDIRECT,
                    headers={'Location': self.login_page,'set-cookie':response.headers['set-cookie']},
                    detail="expired"
                    )  
            if type and type==KeyType.SESSION.value:              
                if username:
                    user = self.get_user(username)
                    if user and not user.disabled:
                        return user
        raise HTTPException(
            status_code=HTTP_307_TEMPORARY_REDIRECT,
            headers={'Location': self.login_page},
            detail="Invalid user"
            )                      
   
    async def logout(self):
        response = Response()
        response.delete_cookie(self.session_cookey)
        raise HTTPException(
            status_code=HTTP_307_TEMPORARY_REDIRECT,
            headers={'Location': self.login_page,'set-cookie':response.headers['set-cookie']})

        
