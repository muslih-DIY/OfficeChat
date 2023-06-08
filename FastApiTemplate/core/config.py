from fastapi import APIRouter,Request,Depends,HTTPException
from datetime import datetime
from typing import Annotated
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from FastApiTemplate.AuthManager import SessionTokenDB,Tokendb, UserInDB,User,Token
from ..AuthManager import LoginManager,UserInDB

class Manager(LoginManager):

    def get_userdb(self, user_id: str) -> UserInDB:
        user = fake_users_db.get(user_id)
        if not user:
            return False
        return UserInDB(**user)
    def get_user(self, user_id: str) -> UserInDB:
        user = self.get_userdb(user_id)
        return User(**user.dict())
    
    def save_session(self,session: SessionTokenDB):
        fake_session_db.update({session.session:session.dict()})

    def save_token(self,token: Tokendb):
        fake_token_db.update({token.access_token:token.dict()})        


    def get_session(self,user:str):
        'return cooies details against a user'
        for session in fake_session_db:
            if session.get('username') == user:
                return SessionTokenDB(**session)
        return None

    def get_token(self,username:str):
        'return token against the user'
        for token in fake_token_db:
            if token.get('username') == username:
                return Tokendb(**token)
        return None

    def get_token_against_session(self,session:str):
        'return token against a cookie' 
        for t,token in fake_token_db.items():
            if token.get('session') == session:
                return Tokendb(**token)
        return None
    

    def invalidate_cookie(self,cookies:str):
        """
        remove cookie from storage and invalidate a session
        remove all the token against the cookies

        """


AuthManager = Manager('auths')

router = APIRouter()

fake_session_db = {
    "session-key":{
        "session":"session-key",
        "user":"johndoe",
        "expiry":"123545673",
        "type":"3" # cookies session
    }
}
fake_token_db = {
    "token":{
        "token":"token",
        "username":"johndoe",
        "expiry":"123545673",
        "session":"token_generated_session"
    }
}

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password":AuthManager.pwd_context.hash('johndoe'),
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password":AuthManager.pwd_context.hash('alice'),
        "disabled": True,
    },
}



@router.get('/token',response_model=Token)
async def get_token(
    request:Request,
    user:User = Depends(AuthManager.get_user_from_cookie)
    ):
    session = request.cookies.get(AuthManager.session_cookey)

    existing_token = AuthManager.get_token_against_session(session)
    
    if existing_token and datetime.fromtimestamp(existing_token.expiry)>datetime.utcnow():
        return existing_token
    access_token = AuthManager.create_access_token(user,'')
    AuthManager.save_token(
        Tokendb(
            **access_token.dict(),
            username= user.username,
            session=session
            )
        )
    return access_token

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    return HTMLResponse(
        """
        <html>
                <form action="/auths" method="post">

                <div class="container">
                    <label for="uname"><b>Username</b></label>
                    <input type="text" placeholder="Enter Username" name="username" required>

                    <label for="psw"><b>Password</b></label>
                    <input type="password" placeholder="Enter Password" name="password" required>

                    <button type="submit">Login</button>
                    <label>
                </div>

                </form>
        </html>
        """
    )

@router.post("/auths", response_class=HTMLResponse)
async def login_for_session_cookies(request:Request,
    form_data:Annotated [OAuth2PasswordRequestForm, Depends()]
):
    user = AuthManager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    session_token = AuthManager.create_session_token(user,'')
    response = RedirectResponse('/',status_code=302)
    print(datetime.fromtimestamp(session_token.expiry).utctimetuple())
    response.set_cookie(
        AuthManager.session_cookey,
        session_token.session,
        expires= datetime.fromtimestamp(session_token.expiry).utctimetuple()
        )
    AuthManager.save_session(session_token)
    print(fake_session_db)
    return response

@router.get("/logout", response_class=HTMLResponse)
async def login_page():
    await AuthManager.logout()

