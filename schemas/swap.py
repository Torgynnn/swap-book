import uuid

from typing import Optional

from .base import Model, ReadModel


class SwapBase(Model):
    receiver_id: uuid.UUID
    offer_book_id: uuid.UUID
    receiver_book_id: uuid.UUID


class SwapCreate(SwapBase):
    pass


class SwapUpdate(SwapBase):
    pass


class SwapRead(SwapBase, ReadModel):
    offer_id: Optional[uuid.UUID]
    receiver_id: Optional[uuid.UUID]
    offer_book_id: Optional[uuid.UUID]
    receiver_book_id: Optional[uuid.UUID]
    status: Optional[str]

    class Config:
        orm_mode = True