from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.authJWT import encode_jwt
from app.celery.worker import send_email
from app.core import get_session
from app.core.settings import app_settings
from app.models import Token, TokenBase, UsersBase
from app.users.confirm import confirm_token_decrypt, confirm_token_encrypt
from app.users.crud import get_register_user, set_register_user, set_user_status
from app.users.utils import token_validation

router = APIRouter(prefix="/api/users", tags=["user"])


http_bearer = HTTPBearer()


@router.post("/register")
def register(data: Annotated[UsersBase, Depends()], db: Session = Depends(get_session)):
    if set_register_user(db, data):
        token_encrypt = confirm_token_encrypt(data.email)
        send_email.delay(token_encrypt)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Пользователь успешно зарегистрирован",
            headers={"X-Error": "There goes my error"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Введите другой email",
            headers={"X-Error": "There goes my error"},
        )


@router.get("/email-verification/{verify_token}")
def email_verification(verify_token: str, db: Session = Depends(get_session)):
    token_decrypt = confirm_token_decrypt(verify_token)
    if token_decrypt:
        set_user_status(db, token_decrypt)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Почта подтверждена",
            headers={"X-Error": "There goes my error"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Нет такого пользователя",
            headers={"X-Error": "There goes my error"},
        )


@router.post("/signin")
def signin(data: UsersBase, db: Session = Depends(get_session)):
    user_auth = get_register_user(db, data)
    if user_auth:
        jwt_payload = {"sub": user_auth.email, "email": user_auth.email}
        access_token = encode_jwt(jwt_payload, expire_minutes=app_settings.access_token_expire_minutes)
        refresh_token = encode_jwt(jwt_payload, expire_minutes=app_settings.refresh_token_expire_minutes)
        return TokenBase(access_token=access_token, refresh_token=refresh_token)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Нет такого пользователя",
            headers={"X-Error": "There goes my error"},
        )


@router.get("/user_info")
def token_validate(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_session)
):
    token = credentials.credentials
    user_info = token_validation(token=token, db=db)
    if user_info:
        return user_info.email
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
            headers={"X-Error": "There goes my error"},
        )


@router.post("/refresh")
def token_refresh(data: Token, db: Session = Depends(get_session)):
    user_info = token_validation(token=data.refresh_token, db=db)
    if user_info:
        jwt_payload = {"sub": user_info.email, "email": user_info.email}
        access_token = encode_jwt(jwt_payload, expire_minutes=app_settings.access_token_expire_minutes)
        refresh_token = encode_jwt(jwt_payload, expire_minutes=app_settings.refresh_token_expire_minutes)
        return TokenBase(access_token=access_token, refresh_token=refresh_token)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
            headers={"X-Error": "There goes my error"},
        )
