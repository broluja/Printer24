from typing import Optional

from src.models.user import User
from src.repository.user_repository import user_repository
from framework.security.security import verify_password


class UserService(object):

    def __init__(self):
        self.user = None
        self.email = None
        self.password = None
        self.company = None

    def authenticate(self) -> Optional[User]:
        user = user_repository.get_by_email(email=self.email)
        verified = verify_password(self.password, user.hashed_password)
        return None if not user or not verified else user
