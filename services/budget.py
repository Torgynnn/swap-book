from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions import BadRequestException
from models import Budget, Book
from schemas import BudgetCreate
from .base import ServiceBase


class BudgetService:
    
    def add_balance(self, db: Session, balance: float, user_id: str) -> Budget:
        budget = db.query(Budget).filter(
            Budget.user_id == user_id
        ).first()

        if budget is None:
            budget = self.create(db, BudgetCreate(user_id=user_id))            
            
        budget.balance = str(float(budget.balance) + (balance))
        
        db.add(budget)
        db.flush()
        
        return budget
    
    def get_by_user(self, db: Session, user_id: str) -> Budget:
        budget = db.query(Budget).filter(
            Budget.user_id == user_id
        ).first()
        
        if budget is None:
            budget = self.create(db, BudgetCreate(user_id=user_id))
        
        return budget
        
    def create(self, db: Session, obj_in: BudgetCreate) -> Budget:
        obj_in_data = jsonable_encoder(obj_in)
        budget = Budget(**obj_in_data)
        
        db.add(budget)
        db.flush()
        
        return budget
        
budget_service = BudgetService()