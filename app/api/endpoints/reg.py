from fastapi import APIRouter, Depends

from app.api.schema import UserReg, RegistrationAnswear
from app.api.src import try_registration, generate_confirmation_token
from app.core.db import get_session, Session
from app.email_task.task import send_email_task

router = APIRouter()

@router.post('users/registration')
def registration(user:UserReg, session:Session = Depends(get_session))->RegistrationAnswear:
    try_registration(user, session)
    conf_url = f'http://localhost/api/email-verification/{generate_confirmation_token(user.email)}'
    body = f'Для подтверждения почты перейдите по ссылке: {conf_url}'
    send_email_task.delay(user.email, body)
    return{
        'answear':'Подтвердите почту'
    }