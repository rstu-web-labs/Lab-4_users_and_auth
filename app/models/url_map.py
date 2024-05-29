from sqlalchemy import Integer, String, Column, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.db import Base

metadata = MetaData()

class Post(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    short_url = Column(String(100), nullable=False, index = True)
    url = Column(String(100), nullable=False)
    created_at = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    click_count = Column(Integer, default=0)

    user = relationship("User", back_populates="posts")

    __table_args__ = (UniqueConstraint('short_url', 'user_id', name='_short_url_user_uc'),)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    session_token = Column(String, unique=True, index=True, nullable=True)

    posts = relationship("Post", back_populates="user")