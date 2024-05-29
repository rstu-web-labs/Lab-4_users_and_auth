from datetime import datetime, timedelta

import jwt

from app.core.settings import app_settings


def encode_jwt(
    payload: dict,
    key: str = app_settings.secret_key,
    algorithm: str = app_settings.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = app_settings.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(token: str | bytes, key: str = app_settings.secret_key, algorithm: str = app_settings.algorithm):
    try:
        decoded_jwt = jwt.decode(token, key, algorithms=algorithm)
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        return False
