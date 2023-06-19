from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException,Request
from fastapi.responses import HTMLResponse,RedirectResponse,FileResponse
from pydantic import BaseModel
from core import config
from core.auth import get_user_from_session
router = APIRouter()


# @router.get("/")
# async def index(user = Depends(get_user_from_session)) -> dict[str, str]:
#     return user

@router.get("/favicon.ico")
async def favcon() -> dict[str, str]:
    return FileResponse(config.STATIC / "icons/favcon.ico")


