
from datetime import datetime
from typing import Annotated
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import APIRouter,Request,Depends,HTTPException
from core import config
from .AccessManager import Manager,Tokendb, User,Token
router = APIRouter()

AuthManager = Manager(
    'auths',
    secret=config.SECRET_KEY,
    algorithm=config.ALGORITHM,
    )

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
        <head>
        </head>
        <body>
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
            </body>
        </html>
        """
    )

@router.post("/auths", response_class=HTMLResponse)
async def login_for_session_cookies(request:Request,
    form_data:Annotated [OAuth2PasswordRequestForm, Depends()]
):
    user = AuthManager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password"
            )
    
    session_token = AuthManager.create_session_token(user,'')
    response = RedirectResponse('/',status_code=302)

    response.set_cookie(
        AuthManager.session_cookey,
        session_token.session,
        expires= datetime.fromtimestamp(session_token.expiry).utctimetuple()
        )
    AuthManager.save_session(session_token)
    return response

@router.get("/logout", response_class=HTMLResponse)
async def login_page():
    await AuthManager.logout()