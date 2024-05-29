from pydantic import BaseModel, EmailStr

class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str