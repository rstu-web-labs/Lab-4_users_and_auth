from fastapi import APIRouter, Depends

from app.api.src import verify_confirmation_token
from app.core.db import Session, get_session
from app.models.user_map import UserModel

router = APIRouter()

@router.get('users/email-verification/{verify_token}')
def verif(verify_token:str, session:Session = Depends(get_session)):
    email = verify_confirmation_token(verify_token)
    user = UserModel(email=email)
    if user.check_user_exists:
        user.change_user_status(session) 
        return {'amswear':'Почта подтверждена'} 
    else:
        raise {'massage':'Несуществующий пользователь'}
