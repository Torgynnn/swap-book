import enum

from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from .base import Model


class SwapStatusEnum(str, enum.Enum):
    PENDING = "Ожидание подтверждения"
    CANCELED = "Отменен"
    APPLIED = "Принят"
    REJECTED = "Отклонен"
    COMPLETED = "Завершен"


class Swap(Model, Base):

    __tablename__ = "swaps"

    offer_id = Column(UUID(as_uuid=True),
                            ForeignKey("users.id"),
                            nullable=False)
    receiver_id = Column(UUID(as_uuid=True),
                            ForeignKey("users.id"),
                            nullable=False)
    offer_book_id = Column(UUID(as_uuid=True),
                        ForeignKey("books.id"),
                        nullable=False)
    receiver_book_id = Column(UUID(as_uuid=True),
                        ForeignKey("books.id"),
                        nullable=False)
    status = Column(Enum(SwapStatusEnum), nullable=False,
                        server_default=SwapStatusEnum.PENDING.value)
    
