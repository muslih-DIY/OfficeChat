from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException,Request
from fastapi.responses import HTMLResponse,RedirectResponse,FileResponse
from pydantic import BaseModel
from core import config
from depends.Auths import AuthManager
from depends.Auths.AccessManager import User
router = APIRouter()


@router.get("/")
async def index(user = Depends(AuthManager.get_user_from_cookie)) -> dict[str, str]:
    return user

@router.get("/favicon.ico")
async def favcon() -> dict[str, str]:
    return FileResponse(config.STATIC / "icons/favcon.ico")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(AuthManager.get_user_from_auth)]
):
    return current_user

