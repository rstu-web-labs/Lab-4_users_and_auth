from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core import get_session
from app.models import OriginalUrlBase, ShortUrlBase
from app.short.crud import get_short_url_join, update_short_counter
from app.short.utils import generate_response_url
from app.users.utils import token_validation

router = APIRouter(prefix="/api/url", tags=["short"])

http_bearer = HTTPBearer(auto_error=False)


@router.get("/{short_url}")
def short_url(short_url: Annotated[ShortUrlBase, Depends()], db: Session = Depends(get_session)):
    if get_short_url_join(db, short_url):
        # print(get_short_url_join(db, short_url))
        update_short_counter(db, short_url.short_url)
        return RedirectResponse(get_short_url_join(db, short_url))
    raise HTTPException(
        status_code=303,
        detail="Короткая ссылка не найдена",
        headers={"X-Error": "There goes my error"},
    )


@router.post("")
def original_url(
    data: Annotated[OriginalUrlBase, Depends()],
    db: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
):
    if credentials:
        token = credentials.credentials
        user = token_validation(token, db)
        if user:
            return generate_response_url(data, db, user.id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found",
                headers={"X-Error": "There goes my error"},
            )
    else:
        return generate_response_url(data, db)
