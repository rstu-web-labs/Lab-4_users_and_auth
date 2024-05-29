from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Users, UsersBase
from app.users.confirm import hash_pswd


def set_register_user(db: Session, data: UsersBase) -> bool:
    try:
        pswd_hash = hash_pswd(data.pswd)
        stmt = insert(Users).values(pswd=pswd_hash, email=str(data.email))
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True


def set_user_status(db: Session, email: str) -> bool:
    try:
        stmt = update(Users).where(Users.email == email).values(status=True)
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True


def get_register_user(db: Session, data: UsersBase):
    pswd_hash = hash_pswd(data.pswd)
    stmt = select(Users).where(Users.email == data.email)
    row = db.execute(stmt).first()
    if row and row[0].pswd == pswd_hash:
        return row[0]
    return False


def get_token_user(db: Session, email: str):
    stmt = select(Users).where(Users.email == email)
    row = db.execute(stmt).first()
    if row:
        return row[0]
    else:
        return False
