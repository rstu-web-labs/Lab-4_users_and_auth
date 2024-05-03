from fastapi import APIRouter, Depends, HTTPException, status

from app.api.src import authenticate_user, create_access_token, create_refresh_token, decode_refresh_token
from app.api.schema import Token, UserReg
from app.core.db import get_session

router = APIRouter()

@router.post("/token")
def login_for_access_token(
    user: UserReg,
    session = Depends(get_session)
)->Token:
    user = authenticate_user(user.email, user.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}, 
    )
    refresh_token = create_refresh_token(data={'sub':user.email})
    return  {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/token/refresh")
async def refresh_token(token:Token)->Token:
    refresh_token_data = decode_refresh_token(token.refresh_token)
    access_token_data = {
        "sub": refresh_token_data["sub"],
    }
    access_token = create_access_token(access_token_data)
    refresh_token_data = {
        "sub": refresh_token_data["sub"],
    }
    refresh_token = create_refresh_token(refresh_token_data)

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }