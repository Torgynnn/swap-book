import uuid

from typing import Optional

from .base import Model, ReadModel


class BudgetBase(Model):
    user_id: uuid.UUID


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BudgetBase):
    pass


class BudgetRead(BudgetBase, ReadModel):
    user_id: Optional[uuid.UUID]
    balance: Optional[str]

    class Config:
        orm_mode = True