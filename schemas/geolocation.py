import uuid

from typing import Optional

from .base import Model, ReadModel


class GeoLocationBase(Model):
    lattd: str
    longtd: str


class GeoLocationCreate(GeoLocationBase):
    pass


class GeoLocationUpdate(GeoLocationBase):
    pass


class GeoLocationRead(GeoLocationBase, ReadModel):
    user_id: Optional[uuid.UUID]
    lattd: Optional[str]
    longtd: Optional[str]

    class Config:
        orm_mode = True