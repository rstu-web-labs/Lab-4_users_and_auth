from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from app.models import OriginalUrl, OriginalUrlBase, ShortUrlBase


def set_original_url(db: Session, data: OriginalUrlBase, user_id: str | None = None) -> bool:
    if user_id:
        stmt = insert(OriginalUrl).values(id_user=int(user_id), url=str(data.url), short_url=str(data.short_url))
    else:
        stmt = insert(OriginalUrl).values(url=str(data.url), short_url=str(data.short_url))
    db.execute(stmt)
    db.commit()
    return True


def get_short_url_in(db: Session, short_url: str):
    stmt = select(OriginalUrl).where(OriginalUrl.short_url == short_url)
    row = db.execute(stmt).first()
    if row:
        return True
    return False


def get_short_url_join(db: Session, data: ShortUrlBase) -> str:
    stmt = select(OriginalUrl).where(OriginalUrl.short_url == data.short_url)
    row = db.execute(stmt).first()
    if row:
        return row[0].url
    return False


def get_short_url_in_all(db: Session, short_urls: List[str]):
    stmt = select(OriginalUrl).where(OriginalUrl.short_url.in_(short_urls))
    row = db.execute(stmt).all()
    found_urls = [item.short_url for item in row]
    if len(found_urls) > 0:
        not_found_url = []
        for item_random in short_urls:
            if item_random not in found_urls:
                not_found_url.append(item_random)
        return not_found_url
    else:
        return short_urls


def update_short_counter(db: Session, short_url: str) -> bool:
    stmt = update(OriginalUrl).where(OriginalUrl.short_url == short_url).values(counter=OriginalUrl.counter + 1)
    db.execute(stmt)
    db.commit()
    return True
