import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import AuthorCreate, AuthorUpdate, AuthorRead
from services import author_service

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AuthorRead],
            summary="Get all Authors")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Authors

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return author_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AuthorRead,
             summary="Create Author")
async def create(*,
                 db: Session = Depends(get_db),
                 body: AuthorCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Author

        - **name**: required
    """
    Authorize.jwt_required()
    return author_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AuthorRead,
            summary="Get Author by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Author by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return author_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AuthorRead,
            summary="Update Author")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: AuthorUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Author

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return author_service.update(
        db,
        db_obj=author_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Author")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Author

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    author_service.remove(db, id)
