from .base import NamedModel, ReadNamedModel


class AuthorBase(NamedModel):
    pass


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorRead(AuthorBase, ReadNamedModel):
    pass

    class Config:
        orm_mode = True