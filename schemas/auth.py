from typing import Optional
from pydantic import EmailStr

from .base import Model


class LoginForm(Model):
    email: EmailStr
    password: str


class RegistrationForm(Model):
    email: EmailStr
    password: str
    re_password: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
