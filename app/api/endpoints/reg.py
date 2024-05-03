from fastapi import APIRouter, Depends

from app.api.schema import UserReg, RegistrationAnswear
from app.api.src import try_registration
from app.core.db import get_session, Session

router = APIRouter()

@router.post('users/registration')
def registration(user:UserReg, session:Session = Depends(get_session))->RegistrationAnswear:
    return try_registration(user, session)