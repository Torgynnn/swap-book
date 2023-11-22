from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions import BadRequestException
from models import GeoLocation, Book
from schemas import GeoLocationCreate
from .base import ServiceBase


class GeoLocationService:
    
    def set_location(self, db: Session, obj_in: GeoLocationCreate, user_id: str) -> GeoLocation:
        self.__delete_present_locations(db, user_id)
        
        obj_in_data = jsonable_encoder(obj_in)
        location = GeoLocation(**obj_in_data)
        location.user_id = user_id
        
        db.add(location)
        db.flush()
        
        return location
    
    def get_by_user(self, db: Session, user_id: str) -> GeoLocation:
        return db.query(GeoLocation).filter(
            GeoLocation.user_id == user_id
        ).first()
    
    def get_all(self, db: Session):
        return (
            db.query(GeoLocation)
            .join(Book, GeoLocation.user_id == Book.publisher_id)
            .filter(
                Book.is_active == True,
            )
            .all()
        )
    
    def __delete_present_locations(self, db: Session, user_id: str):
        db.query(GeoLocation).filter(
            GeoLocation.user_id == user_id
        ).delete()
        
geolocation_service = GeoLocationService()