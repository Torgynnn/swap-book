from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

from core import Base
from .base import Model


class Author(Model, Base):

    __tablename__ = "authors"
    
    books = relationship("Book", back_populates="author",
                            cascade="all, delete")
    name = Column(String, nullable=False, index=True)
