import uuid
import enum
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import BookCreate, BookUpdate, BookRead
from services import book_service

router = APIRouter(
    prefix="/book",
    tags=["Books"],
    dependencies=[
        Depends(
            HTTPBearer())])


class BookSortField(str, enum.Enum):
    BOOK = "book"
    AUTHOR = "author"
    GENRE = "genre"
    
class BookSortOrder(str, enum.Enum):
    ASC = "asc"
    DESC = "desc"


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[BookRead],
            summary="Get all Books")
async def get_all(*,
                  db: Session = Depends(get_db),
                  filter: str = None,
                  skip: int = 0,
                  limit: int = 100,
                  sort_field: BookSortField = None,
                  sort_order: BookSortOrder = None,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Books

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return book_service.get_all(db, filter, sort_field, sort_order, skip, limit)


@router.get("/user/{user_id}", dependencies=[Depends(HTTPBearer())],
            response_model=List[BookRead],
            summary="Get all Books by user")
async def get_by_user(*,
                  db: Session = Depends(get_db),
                  user_id: str,
                  filter: str = None,
                  skip: int = 0,
                  limit: int = 100,
                  sort_field: BookSortField = None,
                  sort_order: BookSortOrder = None,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Books by user

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return book_service.get_by_user(db,
                                    user_id,
                                    filter,
                                    sort_field,
                                    sort_order,
                                    skip,
                                    limit,)


@router.get("/my", dependencies=[Depends(HTTPBearer())],
            response_model=List[BookRead],
            summary="Get all my books")
async def get_my_books(*,
                  db: Session = Depends(get_db),
                  filter: str = None,
                  skip: int = 0,
                  limit: int = 100,
                  sort_field: BookSortField = None,
                  sort_order: BookSortOrder = None,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all my books
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return book_service.get_by_user(db,
                                    user_id,
                                    filter,
                                    sort_field,
                                    sort_order,
                                    skip,
                                    limit) 


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=BookRead,
             summary="Create Book")
async def create(*,
                 db: Session = Depends(get_db),
                 body: BookCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Book

        - **name**: required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return book_service.create(db, body, user_id)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BookRead,
            summary="Get Book by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Book by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return book_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BookRead,
            summary="Update Book")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: BookUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Book

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return book_service.update(
        db,
        db_obj=book_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Book")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Book

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    book_service.delete(db, id)
