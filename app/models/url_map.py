from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.core.db import Base, check_db_connection, engine


class OriginalUrl(Base):
    __tablename__ = "original_short_urls"
    id = mapped_column(Integer, primary_key=True)
    id_user = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    url = mapped_column(String(2048), nullable=False)
    short_url = mapped_column(String(8), nullable=False, unique=True)
    counter = mapped_column(Integer, default=0)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    __table_args__ = (UniqueConstraint("id_user", "short_url"),)

    def to_dict(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "url": self.url,
            "short_url": self.short_url,
            "counter": self.counter,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Users(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    pswd = mapped_column(String(256), nullable=False)
    email = mapped_column(String(126), nullable=False, unique=True)
    status = mapped_column(Boolean, nullable=False, default=False)


def create_database():
    if check_db_connection():
        Base.metadata.create_all(bind=engine)


def delete_tables():
    Base.metadata.drop_all(bind=engine)
