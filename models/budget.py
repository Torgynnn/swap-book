from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from .base import Model


class Budget(Model, Base):

    __tablename__ = "budgets"

    user_id = Column(UUID(as_uuid=True),
                          ForeignKey("users.id"),
                          nullable=False)
    balance = Column(String, nullable=False,
                        server_default="0")
    
    user = relationship("User",
                        foreign_keys=[user_id],
                        back_populates="budget")
