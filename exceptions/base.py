from fastapi import HTTPException


class BaseException(HTTPException):
    pass
