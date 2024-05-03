import base64
from datetime import datetime, timedelta, timezone
from typing import Annotated
import hashlib

import jwt
from sqlalchemy import select
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.api.schema import UserReg, UserInDB
from app.core.db import Session
from app.core.settings import app_settings  
from app.models.user_map import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def try_registration(user:UserReg, session):
    user_model = UserModel(
        email = user.email,
        password = user.password
    )
    if user_model.check_user_exists(session=session):
        raise {'answear':'Пользователь уже зарегистрирован'}
    new_user = user_model.create_new_user(session=session)

def create_access_token(data: dict, expires_delta: timedelta | None = app_settings.access_token_expire_minutes):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app_settings.secret_key, algorithm=app_settings.algorithm)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = app_settings.refresh_token_expire_minutes):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app_settings.secret_key, algorithm=app_settings.algorithm)
    return encoded_jwt

def authenticate_user(username: str, password: str, session):
    user = get_user(username, session)
    user_dict = get_user_dict(user, username)
    
    if not user:
        return False
    if not verify_password(password, user[username]["hashed_password"]):
        return False
    return user_dict

def get_user(login, session:Session):
    with session.begin():
        user = session.execute(select(UserModel).filter(UserModel.email == login)).scalars().first()
        user_db = {
            user.email : {
                "email" : user.email,
                "hashed_password" : user.password,
                "status" : user.status
            }
        }
    return user_db

def get_user_dict(db, email: str):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, app_settings.secret_key, algorithms=["HS256"])
        if datetime.utcfromtimestamp(payload["exp"]) > datetime.utcnow():
            return payload
        else:
            raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload:dict = jwt.decode(token, app_settings.secret_key, algorithms=app_settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(login=username)
    user_dict = get_user_dict(user, username )
    if user is None:
        raise credentials_exception
    return user_dict

def generate_confirmation_token(email: str, secret: str = app_settings.secret_key) -> str:
    email_bytes = email.encode("utf-8")
    email_base64 = base64.urlsafe_b64encode(email_bytes)
    email_base64_str = email_base64.decode("utf-8").rstrip("=")

    token_data = email_base64_str + secret
    token_bytes = token_data.encode("utf-8")
    token_hash = hashlib.sha256(token_bytes).hexdigest()

    return f"{email_base64_str}-{token_hash}"

def verify_confirmation_token(token: str, secret: str = app_settings.secret_key) -> str:
    token_parts = token.split("-")
    if len(token_parts) != 2:
        raise ValueError("Invalid token format")
    email_base64_str, token_hash = token_parts

    email_base64_bytes = email_base64_str.encode("utf-8")
    email_bytes = base64.urlsafe_b64decode(email_base64_bytes + b"==")
    email = email_bytes.decode("utf-8")

    token_data = email_base64_str + secret
    token_bytes = token_data.encode("utf-8")
    expected_hash = hashlib.sha256(token_bytes).hexdigest()
    if token_hash != expected_hash:
        raise ValueError("Invalid token")

    return email