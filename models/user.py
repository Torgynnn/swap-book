from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from .base import Model


class User(Model, Base):

    __tablename__ = "users"

    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    phone_number = Column(String(32))
    
    books = relationship("Book", back_populates="publisher",
                            cascade="all, delete")
    budget = relationship("Budget", uselist=False, back_populates="user",
                            cascade="all, delete")
    geolocation = relationship("GeoLocation", back_populates="user",
                            cascade="all, delete")
