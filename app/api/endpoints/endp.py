from typing import Optional

from fastapi import APIRouter, Depends, Security
from fastapi.responses import RedirectResponse

from app.api.schema import ShortURL, User
from app.api.src import get_current_user
from app.url import generate_short_link
from app.models import get_original_url
from app.core.db import get_session, Session

router = APIRouter()

@router.get('/{short_url}', tags=['Перейти по новой ссылке'])
def get(short_url:str, token:str|None = None, session:Session = Depends(get_session))->ShortURL:
    user = get_current_user(token, session)
    return RedirectResponse(url = get_original_url(short_url, user, session))

@router.post('', tags=['Создать короткую ссылку'])
def post(url:str, token:str|None = None, session:Session = Depends(get_session))->ShortURL:
    user = get_current_user(token, session)
    return generate_short_link(url, user, session)

