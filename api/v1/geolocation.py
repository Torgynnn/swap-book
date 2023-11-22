import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import GeoLocationRead, GeoLocationCreate
from services import geolocation_service

router = APIRouter(
    prefix="/geolocations",
    tags=["GeoLocations"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[GeoLocationRead],
            summary="Get all GeoLocations")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all GeoLocations

       - **skip**: int - The number of GeoLocations
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of GeoLocations
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return geolocation_service.get_all(db)


@router.get("/{user_id}/", dependencies=[Depends(HTTPBearer())],
            response_model=GeoLocationRead,
            summary="Get GeoLocation by user id")
async def get_by_user_id(*,
                    db: Session = Depends(get_db),
                    user_id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get GeoLocation by id

        - **user_id**: UUID - required
    """
    Authorize.jwt_required()
    return geolocation_service.get_by_user(db, user_id)


@router.post("", dependencies=[Depends(HTTPBearer())],
                response_model=GeoLocationRead,
                summary="Set GeoLocation")
async def set_location(*,
                    db: Session = Depends(get_db),
                    body: GeoLocationCreate,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Set GeoLocation
        
        - **obj_in**: GeoLocationCreate - required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return geolocation_service.set_location(db, body, user_id)
