from sqlalchemy import Column, String, DateTime, Integer, Table
from app.core.db import Base
from sqlalchemy.sql import func


class UrlMap(Base):
    __tablename__ = 'url_map'

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_url = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
