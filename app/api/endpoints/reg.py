from fastapi import APIRouter

from app.api.schema import User, RegistrationAnswear

router = APIRouter()

@router.post('/registration')
def registration(user:User)->RegistrationAnswear:
    pass