import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from framework.database.settings import Base


class Organisation(Base):
    """ Model for data table 'organisations' """
    __tablename__ = "organisations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
