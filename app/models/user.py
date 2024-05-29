from sqlalchemy import Boolean, Column, String, Integer
from app.core.db import Base

class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    email_verification_token = Column(String)  # Добавленный столбец
    email_verified = Column(Boolean, default=False)  # Добавленный столбец

    @classmethod
    def get_by_email(cls, email: str):
        return cls.query.filter(cls.email == email).first()

    def confirm_email(self):
        # Установить флаг подтверждения адреса электронной почты на True
        self.email_verified = True


__all__ = ["User"]
