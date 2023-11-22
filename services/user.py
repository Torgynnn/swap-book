from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions import BadRequestException
from models import User
from schemas import UserCreate, UserUpdate, BudgetCreate
from .base import ServiceBase
from .budget import budget_service


class UserService(ServiceBase[User, UserCreate, UserUpdate]):
    
    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(
            User.email == email
        ).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        user = self.model(**obj_in_data)
        
        db.add(user)
        db.flush()
        
        budget_service.create(db, BudgetCreate(user_id=user.id))
        
        return user

user_service = UserService(User)