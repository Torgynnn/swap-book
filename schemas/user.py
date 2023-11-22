from typing import Optional, List

from .base import Model, ReadModel
from schemas import BookRead, BudgetRead

class UserBase(Model):
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str]


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserRead(UserBase, ReadModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    books: Optional[List[BookRead]]
    budget: Optional[BudgetRead]
    
    class Config:
        orm_mode = True
