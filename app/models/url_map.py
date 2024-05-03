from sqlalchemy import Integer, String, DateTime, select, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.core.db import Base, Session

class ShortUrl(Base):
    __tablename__="short_url"
    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String(255), nullable=False, unique=True)
    short_url = mapped_column(String(8), nullable=False, unique=True)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
    user_id = mapped_column(ForeignKey('user.id', ondelete='cascade'))
    __table_args__ = (
        UniqueConstraint('short_url', 'user_id', name='uix_short_url_user_id'),
    )

def get_original_url(short_url, session:Session):
    with session.begin():
        short_url_obj = session.execute(select(ShortUrl).filter(ShortUrl.short_url==short_url)).scalars().first()
    return short_url_obj

def add_short_url(url, short_url, session:Session):
    new_short_url = ShortUrl(url=url, short_url=short_url)
    with session.begin():
        session.add(new_short_url)
        session.commit()