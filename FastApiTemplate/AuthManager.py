from typing import Dict, Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from fastapi import Request
from abc import ABC,abstractmethod


class OAuth2Manager(OAuth2PasswordBearer,ABC):
    
    def __init__(self, tokenUrl: str, scheme_name: str | None = None, scopes: Dict[str, str] | None = None, description: str | None = None, auto_error: bool = True):
        super().__init__(tokenUrl, scheme_name, scopes, description, auto_error)
    
    def create_access_token(self,data):
        return "ABC"+str(data)
    def create_session_cookie(self,data):
        return "ABC"+str(data)
    
    async def get_session_cookie(self, request: Request) -> Optional[str]:
        authorization = request.session.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param

    async def get_header_token(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param

