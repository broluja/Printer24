import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from framework.database.settings import Base


class User(Base):
    """ Model for data table 'users' """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(ForeignKey('organisations.id'), unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)
    is_superuser = Column(Boolean, default=False)
    has_color = Column(Boolean, default=False)
    limit = Column(Integer, default=50)
    code = Column(Integer, unique=True)

    organisation = relationship('Organisation', foreign_keys=[company])

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_superuser': self.is_superuser,
            'company_id': self.company
        }
