from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..core.config import Session_manager
from ..AuthManager import User
router = APIRouter()


@router.get("/")
async def index(user = Depends(Session_manager.get_user_from_cookie)) -> dict[str, str]:
    return user

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
@router.get("/logout", response_class=HTMLResponse)
async def login_page():
    await Session_manager.logout()

@router.post("/auths", response_class=HTMLResponse)
async def login_for_session_cookies(request:Request,
    form_data:Annotated [OAuth2PasswordRequestForm, Depends()]
):
    user = Session_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token,expire = Session_manager.create_session_token(user,'')
    response = RedirectResponse('/',status_code=302)
    response.set_cookie(
        Session_manager.session_cookey,
        access_token,
        expires=expire.utcfromtimestamp
        )
    return response

@router.get('/token',response_model=Token)
async def get_token(
    request:Request,
    user = Depends(Session_manager.get_user_from_cookie)
    ):

    token,expiry = Session_manager.create_access_token(user,'')
    return {"access_token": token, "token_type": "bearer","expiry":expiry}


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(Session_manager.get_user_from_auth)]
):
    return current_user

