from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.authJWT import decode_jwt
from app.users.crud import get_token_user


def token_validation(token: str, db: Session):
    try:
        payload = decode_jwt(token)
    except InvalidTokenError:
        return False
    if payload:
        user = get_token_user(db, payload.get("email"))
    else:
        return False
    if user:
        return user
    else:
        return False
