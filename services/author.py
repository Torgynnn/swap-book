from sqlalchemy.orm import Session

from models import Author
from schemas import AuthorCreate, AuthorUpdate
from .base import ServiceBase


class AuthorService(ServiceBase[Author, AuthorCreate, AuthorUpdate]):
    pass


author_service = AuthorService(Author)