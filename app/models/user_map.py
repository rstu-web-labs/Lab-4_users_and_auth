from sqlalchemy import Integer, String, Boolean, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapped_column
from passlib.context import CryptContext

from app.core.db import Base, Session

pwd_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    status = mapped_column(Boolean, nullable=False, default=False)

    def check_user_exists(self,session:Session):
        with session.begin():
            user = session.execute(select(UserModel).filter(UserModel.email == self.email)).scalars().first()
        return True if user else False
    
    def create_new_user(self,session:Session):
        user = UserModel(
            email = self.email,
            password = pwd_context.hash(self.password),
            status = False
        )
        with session.begin():
            try:
                session.add(user)
                session.commit()
                return user
            except IntegrityError as e:
                session.rollback()
                raise {"IntegrityError:":e}
    
    def change_user_status(self, status: bool, session:Session):
        with session.begin():
            user = session.execute(select(UserModel).filter(UserModel.email == self.email)).scalars().first()
            user.status = status
            session.commit()