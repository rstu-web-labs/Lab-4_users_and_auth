from fastapi import APIRouter, Depends

from app.core.db import get_session, Session
from app.api.src import get_current_user
from app.email_task.task import send_report_task

router = APIRouter()

@router.get('/report')
def report(token:str, session:Session = Depends(get_session)):
    user = get_current_user(token, session)
    send_report_task.delay(user.email)
    return {'answear':'Отчет отправлен на почту'}
