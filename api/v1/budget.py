import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import BudgetRead, BudgetCreate
from services import budget_service

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("/{user_id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BudgetRead,
            summary="Get Budget by user id")
async def get_by_user_id(*,
                    db: Session = Depends(get_db),
                    user_id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Budget by id

        - **user_id**: UUID - required
    """
    Authorize.jwt_required()
    return budget_service.get_by_user(db, user_id)


@router.patch("/{user_id}", dependencies=[Depends(HTTPBearer())],
                response_model=BudgetRead,
                summary="Set Budget")
async def add_balance(*,
                    db: Session = Depends(get_db),
                    user_id: uuid.UUID,
                    balance: float,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Set Budget
        
        - **obj_in**: BudgetCreate - required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return budget_service.add_balance(db, balance, user_id)
