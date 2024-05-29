from typing import List, Optional

import re

from pydantic import BaseModel, EmailStr, HttpUrl, conint, constr, field_validator

from fastapi import  HTTPException, status


class OriginalUrlBase(BaseModel):
    url: HttpUrl
    short_url: Optional[constr(pattern=r"^[a-zA-Z0-9]+$", max_length=8)] = None


class CustomUrlBase(BaseModel):
    url: HttpUrl
    custom_url: Optional[constr(pattern=r"^[a-zA-Z0-9]+$", max_length=8)] = None
    share_url: HttpUrl | str = ""


class ShortUrlBase(BaseModel):
    short_url: constr(pattern=r"^[a-zA-Z0-9]+$", max_length=8)


class UsersBase(BaseModel):
    pswd: str
    email: EmailStr
    
    @field_validator("pswd")
    def check_password(cls, value):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        if not re.match(pattern, value):
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="длинна пароля должны быть не менее 8 символов и включать хотя бы одну маленькую английскую букву, хотя бы одну большую и хотя бы одну цифру.",
        )
        return value
        


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str = "null"
    token_type: str = "Bearer"


class Token(BaseModel):
    refresh_token: str


class MetricsBase(BaseModel):
    order: str | None = "desc"
    limit: conint(ge=1, le=50)
    offset: int
    type: str | None = "all"


class RequestBase(BaseModel):
    founded: int | None = 1
    previous: str | None = "null"
    next: str | None = "null"
    items: List | None
