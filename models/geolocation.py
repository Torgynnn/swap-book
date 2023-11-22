from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from .base import Model


class GeoLocation(Model, Base):

    __tablename__ = "geolocations"

    user_id = Column(UUID(as_uuid=True),
                          ForeignKey("users.id"),
                          nullable=False)
    lattd = Column(String, nullable=False)
    longtd = Column(String, nullable=False)

    user = relationship("User",
                        foreign_keys=[user_id],
                        back_populates="geolocation")