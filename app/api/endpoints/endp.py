from fastapi import APIRouter, Depends

from app.api.schema import ShortURL
from app.url import generate_short_link
from app.models import get_original_url
from app.core.db import get_session, Session

router = APIRouter()

@router.get('/{short_url}', tags=['Перейти по новой ссылке'])
def get(short_url:str, session:Session = Depends(get_session))->ShortURL:
    return get_original_url(short_url, session)

@router.post('', tags=['Создать короткую ссылку'])
def post(url:str, session:Session = Depends(get_session))->ShortURL:
    return generate_short_link(url, session)

