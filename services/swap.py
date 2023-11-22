import uuid

from typing import Any, Dict, Union
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions import BadRequestException
from models import Swap, SwapStatusEnum
from schemas import SwapCreate, SwapUpdate
from .base import ServiceBase
from .user import user_service
from .book import book_service
from .budget import budget_service

class SwapService(ServiceBase[Swap, SwapCreate, SwapUpdate]):
    
    def get_inbox(self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.receiver_id == user_id
        ).offset(skip).limit(limit).all()
        
    def get_outbox(self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.offer_id == user_id
        ).offset(skip).limit(limit).all()
    
    def set_status(self, db: Session, id: str, status: SwapStatusEnum):
        swap = self.get_by_id(db, id)
        swap.status = status.value
        
        if status == SwapStatusEnum.COMPLETED:
            offer_book = book_service.get_by_id(db, swap.offer_book_id)
            receiver_book = book_service.get_by_id(db, swap.receiver_book_id)
            
            offer_book.is_active = False
            receiver_book.is_active = False
            
            offer_budget = budget_service.get_by_user(db, swap.offer_id)
            receiver_budget = budget_service.get_by_user(db, swap.receiver_id)
            
            budget_service.add_balance(db, 300.0, offer_budget.user_id)
            budget_service.add_balance(db, 300.0, receiver_budget.user_id)
            
            db.add(offer_book)
            db.add(receiver_book)
        
        db.add(swap)
        db.flush()
        
        return swap
    
    def create(self, db: Session, obj_in: SwapCreate, user_id: str) -> Swap:
        self.__validate_create(db, obj_in, user_id)
        
        obj_in_data = jsonable_encoder(obj_in)
        swap = self.model(**obj_in_data)
        swap.offer_id = user_id
        swap.status = SwapStatusEnum.PENDING.value
        
        db.add(swap)
        db.flush()
        
        return swap
    
    def __validate_create(self, db: Session, obj_in: SwapCreate, user_id: str) -> Swap:
        offer = user_service.get_by_id(db, user_id)
        offer_book = book_service.get_by_id(db, obj_in.offer_book_id)
        receiver = user_service.get_by_id(db, obj_in.receiver_id)
        receiver_book = book_service.get_by_id(db, obj_in.receiver_book_id)
        
        print(str(offer_book.publisher_id) != user_id)
        if str(offer_book.publisher_id) != user_id:
            print(offer_book.publisher_id)
            print(user_id)
            raise BadRequestException("This book is not yours")
        if str(receiver_book.publisher_id) != str(obj_in.receiver_id):
            raise BadRequestException("This book is not receiver's")

swap_service = SwapService(Swap)