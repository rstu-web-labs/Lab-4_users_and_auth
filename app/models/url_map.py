from sqlalchemy import Integer, String, DateTime, select, ForeignKey, UniqueConstraint, and_
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.core.db import Base, Session
from app.models.user_map import UserModel

class ShortUrl(Base):
    __tablename__="short_url"
    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String(255), nullable=False)
    short_url = mapped_column(String(8), nullable=False, unique=True)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
    user_id = mapped_column(ForeignKey('user.id', ondelete='cascade'))
    redirect_count = mapped_column(Integer, default=0)
    __table_args__ = (
        UniqueConstraint('short_url', 'user_id', name='uix_short_url_user_id'),
    )

def get_original_url(short_url, user, session:Session):
    with session.begin():
        if not user:
            short_url_obj = session.execute(select(ShortUrl).filter(ShortUrl.short_url==short_url)).scalars().first()
            short_url_obj.redirect_count += 1
            session.commit()
        else:
            user_id = session.execute(select(UserModel).filter(UserModel.email==user.email)).scalars().first().id
            short_url_obj = session.execute(select(ShortUrl).where(and_(ShortUrl.short_url==short_url, ShortUrl.user_id == user_id))).scalars().first()
            short_url_obj.redirect_count += 1
            session.commit()
    return short_url_obj.url

def get_short_url(original_url, session:Session):
    with session.begin():
        url_obj = session.execute(select(ShortUrl).filter(ShortUrl.url==original_url)).scalars().first()
    return url_obj

def add_short_url(url, short_url, session:Session):
    new_short_url = ShortUrl(url=url, short_url=short_url)
    with session.begin():
        session.add(new_short_url)
        session.commit()

def add_short_url_auth(url, short_url, user, session:Session):
    with session.begin():
        user_id = session.execute(select(UserModel).filter(UserModel.email==user.email)).scalars().first().id
        new_short_url = ShortUrl(url=url, short_url=short_url, user_id = user_id)
        session.add(new_short_url)
        session.commit()
    return user_id