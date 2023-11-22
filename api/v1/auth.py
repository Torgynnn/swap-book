from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (LoginForm,
                     RegistrationForm, UserRead)
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login", summary="Login")
async def login(form: LoginForm,
                db: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()):
    """
    Login to the system.

    - **email**: required and should be a valid email format.
    - **password**: required.
    """
    return auth_service.login(form, db, Authorize)


@router.post("/register", summary="Register", response_model=UserRead)
async def register(form: RegistrationForm, db: Session = Depends(get_db)):
    """
        Register new user to the system.

        - **email**: string required and should be a valid email format.
        - **first_name**: required.
        - **last_name**: required.
        - **father_name**: optional.
        - **password**: required.
        - **re_password**: required and should match the password field.
    """
    return auth_service.register(form, db)


@router.get('/refresh', dependencies=[Depends(HTTPBearer())])
def refresh_token(Authorize: AuthJWT = Depends(),
                  db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token")

    return auth_service.refresh_token(db, Authorize)