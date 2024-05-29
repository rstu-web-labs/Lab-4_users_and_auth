from pydantic import BaseModel, EmailStr

class Config:
    arbitrary_types_allowed = True

class ShortURL(BaseModel, Config):
    url:str
    short_url:str
    share_url:str | None

class UserReg(BaseModel, Config):
    email: EmailStr
    password: str
    status: bool | None = None

class User(BaseModel, Config):
    email:EmailStr
    
class UserInDB(User, Config):
    hashed_password: str

class RegistrationAnswear(BaseModel, Config):
    answear:str | None = None

class Token(Config, BaseModel):
    access_token: str
    refresh_token: str
    token_type: str