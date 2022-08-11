from typing import Optional

from src.models.user import User
from src.repository.base_repository import CRUDBase


class UserRepository(CRUDBase[User]):
    """ CRUD`s subclass for interaction with 'users' table """
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_uid(self, uid: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == uid).first()

    def get_by_code(self, code: int) -> Optional[User]:
        return self.db.query(User).filter(User.code == code).first()


user_repository = UserRepository(User)
