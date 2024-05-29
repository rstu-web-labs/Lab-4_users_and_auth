import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.celery.worker import send_excel
from app.core import get_session
from app.metrics.crud import get_shorts_all, get_shorts_user
from app.models import MetricsBase, RequestBase
from app.users.utils import token_validation

http_bearer = HTTPBearer()

router = APIRouter(prefix="/api", tags=["metrics"])


@router.get("/url-leaders")
def leaders(data: Annotated[MetricsBase, Depends()], db: Session = Depends(get_session)):
    items, count = get_shorts_all(db, data)
    data_request = RequestBase(items=items)
    data_request.founded = int(count / data.limit)
    data_request.previous = f"http://localhost:8005/api/url-leaders?order={data.order}&limit={data.limit}&offset={data.offset-data.limit if data.offset-data.limit >= 0 and data.offset-data.limit < count else 0}&type={data.type}"
    data_request.next = f"http://localhost:8005/api/url-leaders?order={data.order}&limit={data.limit}&offset={data.offset+data.limit if data.offset+data.limit <= count-1 else count-1}&type={data.type}"
    return data_request


@router.get("/report-user")
def report_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_session)):
    token = credentials.credentials
    user_info = token_validation(token=token, db=db)
    user_all = get_shorts_user(db, user_info.email)
    user_all_serializable = [original_url.to_dict() for original_url in user_all]
    user_all_json = json.dumps(user_all_serializable)
    send_excel.delay(user_info.email, user_all_json)
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Задача на отправку почты запущена!",
        headers={"X-Error": "There goes my error"},
    )
    # set_exel_report(user_info.email, user_all)
    # print(user_info.email)
