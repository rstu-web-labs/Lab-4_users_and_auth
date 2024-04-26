from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column
from app.core.db import Base

class UserModel(Base):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    status = mapped_column(Boolean, nullable=False, default=False)