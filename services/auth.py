from datetime import timedelta

from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from models import User
from schemas import LoginForm, RegistrationForm, UserCreate
from exceptions import BadRequestException
from core import configs
from .user import user_service
from utils import hash_password, is_valid_phone_number, verify_password


class AuthService:
    
    
    def login(self, form: LoginForm, db: Session, Authorize: AuthJWT):
        user = user_service.get_by_email(db, EmailStr(form.email).lower())

        if not user:
            raise BadRequestException(detail="Incorrect email or password!")
        if not verify_password(form.password, user.password):
            raise BadRequestException(detail='Incorrect email or password')

        access_token, refresh_token = self.__generate_tokens(Authorize, user)

        return {"access_token": access_token, "refresh_token": refresh_token}
    
    
    def register(self, form: RegistrationForm, db: Session):

        if user_service.get_by_email(db, EmailStr(form.email).lower()):
            raise BadRequestException(
                detail="User with this email already exists!")
        if form.phone_number and not is_valid_phone_number(form.phone_number):
            raise BadRequestException(detail="Invalid phone number!")
        if form.password != form.re_password:
            raise BadRequestException(detail="Password mismatch!")
        
        user_obj_in = UserCreate(
            email=EmailStr(form.email).lower(),
            first_name=form.first_name,
            last_name=form.last_name,
            phone_number=form.phone_number,
            password=hash_password(form.password)
        )
        
        user = user_service.create(db=db, obj_in=user_obj_in)
        
        return user
    
    
    def refresh_token(self, db: Session, Authorize: AuthJWT):
        if not Authorize.get_jwt_subject():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        
        user = user_service.get(db, Authorize.get_jwt_subject())
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='The user belonging to this token no longer exist')

        access_token, refresh_token = self.__generate_tokens(Authorize, user)

        return {"access_token": access_token, "refresh_token": refresh_token}


    def __generate_tokens(self, Authorize: AuthJWT, user: User):

        user_claims = {
            "id": str(user.id),
        }
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            user_claims=user_claims,
            expires_time=timedelta(minutes=configs.ACCESS_TOKEN_EXPIRES_IN)
        )
        refresh_token = Authorize.create_refresh_token(
            subject=str(user.id),
            user_claims=user_claims,
            expires_time=timedelta(minutes=configs.REFRESH_TOKEN_EXPIRES_IN)
        )

        return access_token, refresh_token


auth_service = AuthService()
