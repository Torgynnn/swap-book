import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import SwapStatusEnum
from schemas import SwapCreate, SwapUpdate, SwapRead
from services import swap_service

router = APIRouter(
    prefix="/swaps",
    tags=["Swaps"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[SwapRead],
            summary="Get all Swaps")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Swaps

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return swap_service.get_multi(db, skip, limit)


@router.get("/inbox", dependencies=[Depends(HTTPBearer())],
            response_model=List[SwapRead],
            summary="Get all Swaps in inbox")
async def get_inbox(*,
                    db: Session = Depends(get_db),
                    skip: int = 0,
                    limit: int = 100,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get all Swaps in inbox
        
        - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return swap_service.get_inbox(db, user_id, skip, limit) 


@router.get("/outbox", dependencies=[Depends(HTTPBearer())],
            response_model=List[SwapRead],
            summary="Get all Swaps in outbox")
async def get_outbox(*,
                    db: Session = Depends(get_db),
                    skip: int = 0,
                    limit: int = 100,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get all Swaps in outbox
        
        - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return swap_service.get_outbox(db, user_id, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SwapRead,
             summary="Create Swap")
async def create(*,
                 db: Session = Depends(get_db),
                 body: SwapCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Swap

        - **name**: required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return swap_service.create(db, body, user_id)


@router.patch("/{id}/status", dependencies=[Depends(HTTPBearer())],
                response_model=SwapRead,
                summary="Set Swap status")
async def set_status(*,
                        db: Session = Depends(get_db),
                        id: uuid.UUID,
                        status: SwapStatusEnum,
                        Authorize: AuthJWT = Depends()
                        ):
        """
            Set Swap status
    
            - **id**: UUID - required
            - **status**: str - required
        """
        Authorize.jwt_required()
        return swap_service.set_status(db, id, status)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SwapRead,
            summary="Get Swap by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Swap by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return swap_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SwapRead,
            summary="Update Swap")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: SwapUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Swap

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return swap_service.update(
        db,
        db_obj=swap_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Swap")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Swap

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    swap_service.remove(db, id)
