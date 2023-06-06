from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..core.config import AuthManager
from ..AuthManager import User
router = APIRouter()


@router.get("/")
async def index(user = Depends(AuthManager.get_user_from_cookie)) -> dict[str, str]:
    return user


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(AuthManager.get_user_from_auth)]
):
    return current_user

