import logging

from fastapi import Request, HTTPException
from fastapi.security.base import SecurityBase
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional
from fastapi.openapi.models import SecurityBase as SecurityBaseModel

from framework.exceptions.exceptions import ServerException
from framework.security.security import validate_token
from src.repository.user_repository import user_repository

logger = logging.getLogger('documents-api')


class Authenticated:
    def __init__(self, token: str):
        self.token = token
        if not token:
            raise ServerException(message="Token Missing", status_code=401)

        try:
            self.user = self.validate_user()
        except Exception as e:
            raise ServerException(message=str(e), status_code=401) from e

    def validate_user(self):
        email = validate_token(self.token)
        if user := user_repository.get_by_email(email):
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")


class SuperUser(Authenticated):
    def __init__(self, token: str):
        super().__init__(token)
        self.validate_superuser()

    def validate_superuser(self):
        if not self.user.is_superuser:
            raise ServerException(message="Superuser status missing", status_code=401)
        return True


class SuperAdmin(object):
    pass


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.model = SecurityBaseModel(type="http")

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param
