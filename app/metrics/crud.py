from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import MetricsBase, OriginalUrl, Users


def row_to_dict(item):
    data = {
        "url": item.url,
        "custom_url": item.short_url,
        "share_url": (
            f"http://0.0.0.0:8005/api/url/{item.short_url}?u={item.id_user}"
            if item.id_user != None
            else f"http://0.0.0.0:8005/api/url/{item.short_url}"
        ),
        "user_id": item.id_user,
        "counter": item.counter,
    }
    return data


def get_shorts_all(db: Session, data: MetricsBase):
    stmt = (
        select(OriginalUrl)
        .where(
            OriginalUrl.id_user != None
            if data.type == "users"
            else OriginalUrl.id_user == None if data.type == "anonim" else True
        )
        .order_by(OriginalUrl.counter.desc() if data.order == "desc" else OriginalUrl.counter.asc())
        .offset(data.offset)
        .limit(data.limit)
    )
    row = db.execute(stmt).all()
    data_all = [row_to_dict(item[0]) for item in row]
    stmt = (
        select(func.count())
        .select_from(OriginalUrl)
        .where(
            OriginalUrl.id_user != None
            if data.type == "users"
            else OriginalUrl.id_user == None if data.type == "anonim" else True
        )
    )
    count = db.execute(stmt).first()
    return data_all, count[0]


def get_shorts_user(db: Session, email: str):
    stmt = select(Users.id).where(Users.email == email).scalar_subquery()
    main_stmt = select(OriginalUrl, stmt).where(OriginalUrl.id_user == stmt)
    row = db.execute(main_stmt).all()
    user_all = [item[0] for item in row]
    return user_all
