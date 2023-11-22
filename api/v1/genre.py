import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import GenreCreate, GenreUpdate, GenreRead
from services import genre_service

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[GenreRead],
            summary="Get all Genres")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Genreize: AuthJWT = Depends()
                  ):
    """
       Get all Genres

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Genreize.jwt_required()
    return genre_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=GenreRead,
             summary="Create Genre")
async def create(*,
                 db: Session = Depends(get_db),
                 body: GenreCreate,
                 Genreize: AuthJWT = Depends()
                 ):
    """
        Create Genre

        - **name**: required
    """
    Genreize.jwt_required()
    return genre_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=GenreRead,
            summary="Get Genre by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Genreize: AuthJWT = Depends()
                    ):
    """
        Get Genre by id

        - **id**: UUID - required
    """
    Genreize.jwt_required()
    return genre_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=GenreRead,
            summary="Update Genre")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: GenreUpdate,
                 Genreize: AuthJWT = Depends()
                 ):
    """
        Update Genre

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Genreize.jwt_required()
    return genre_service.update(
        db,
        db_obj=genre_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Genre")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Genreize: AuthJWT = Depends()
                 ):
    """
        Delete Genre

        - **id**: UUID - required
    """
    Genreize.jwt_required()
    genre_service.remove(db, id)
