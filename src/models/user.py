import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from framework.database.settings import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)
    is_superuser = Column(Boolean, default=False)

    # plan = relationship("BillingPlan", foreign_keys=[billing_plan_id])
    # c_via_secondary = relationship("Permission", secondary="billing_plans",
    #                                primaryjoin="User.billing_plan_id == BillingPlan.id",
    #                                secondaryjoin="Permission.billing_plan_id == BillingPlan.id",
    #                                viewonly=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_superuser": self.is_superuser,
        }
