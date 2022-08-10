from typing import Optional

from src.models.user import User
from src.repository.user_repository import user_repository


class UserService:

    def __init__(self):
        self.user = None
        self.email = None
        self.password = None
        self.test = None
        self.duration = None

    def authenticate(self) -> Optional[User]:
        if user := user_repository.get_by_email(email=self.email):
            return user
        return None
