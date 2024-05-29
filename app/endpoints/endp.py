from fastapi import APIRouter, HTTPException, Header, Depends, Query
from app.models.url_map import Post, User
from app.schemas.url import UrlOut, UrlIn
from app.core.db import SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc
import random
import string
import base64
from datetime import date
from fastapi.responses import RedirectResponse
from app.core.security import verify_token_signature, validate_password, hash_password
from app.schemas.users import UserRegisterIn
from app.tasks import send_confirmation_email
from sqlalchemy.orm import Session
import secrets
from app.tasks import send_user_report
from app.core.settings import SECRET_KEY, APP_EXTERNAL_PORT

router = APIRouter()

def get_current_user(session_token: str = Header(None)):
    if not session_token:
        return None

    session = SessionLocal()
    user = session.query(User).filter(User.session_token == session_token).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

def generate_short_url(length: int = 8):
    short_url = ''
    while len(short_url) < length:
        short_url += random.choice(string.ascii_letters + string.digits)
    return short_url

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_session_token():
    return secrets.token_urlsafe(32)

@router.post("/api/url/", response_model=UrlOut)
async def create_url(url_in: UrlIn, db: Session = Depends(get_db), session_token: str = Header(None)):
    user_id = None
    if session_token:
        user = db.query(User).filter(User.session_token == session_token).first()
        if user:
            user_id = user.id

    short_url = url_in.short_url if url_in.short_url else generate_short_url()
    while db.query(Post).filter(Post.short_url == short_url, Post.user_id == user_id).first():
        short_url = generate_short_url()

    url = Post(short_url=short_url, url=url_in.url, created_at=str(date.today()), user_id=user_id)
    try:
        db.add(url)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Не удалось создать URL")

    share_url = f"http://localhost:{APP_EXTERNAL_PORT}/api/url/{short_url}"
    if user_id:
        share_url += f"?u={user_id}"

    return UrlOut(short_url=short_url, url=url.url, created_at=url.created_at, share_url=share_url)

@router.get("/api/url/{short_url}", response_model=UrlOut)
async def get_url(short_url: str, db: Session = Depends(get_db)):
    url = db.query(Post).filter(Post.short_url == short_url).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.click_count += 1
    db.commit()

    return RedirectResponse(url.url)


@router.post("/api/users/register/")
async def register_user(user_in: UserRegisterIn, db: Session = Depends(get_db)):
    # Валидация пароля
    if not validate_password(user_in.password):
        raise HTTPException(status_code=400, detail="Пароль должен быть не менее 8 символов и содержать хотя бы одну маленькую английскую букву, одну большую и одну цифру.")

    hashed_password = hash_password(user_in.password)

    try:
        user = User(email=user_in.email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    send_confirmation_email.delay(user_in.email)

    return {"message": "Пользователь успешно зарегистрирован. Пожалуйста, проверьте свою почту для подтверждения."}


@router.get("/api/users/email-verification/{verify_token}")
async def email_verification(verify_token: str, db: Session = Depends(get_db)):
    # разделение токена
    email_baseencode, signature = verify_token.split("-")
    
    email = base64.b64decode(email_baseencode).decode()

    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if verify_token_signature(email_baseencode, signature, SECRET_KEY):
        user.email_verified = True
        user.session_token = generate_session_token() 
        db.commit()
        return {"message": "Адрес электронной почты успешно подтвержден", "session_token": user.session_token}
    else:
        raise HTTPException(status_code=400, detail="Неверная подпись токена")

@router.get("/api/url-leaders", response_model=dict)
async def get_url_leaders(
    order: str = Query("desc", regex="^(asc|desc)$"),
    limit: int = Query(..., ge=1, le=50),
    offset: int = Query(..., ge=0),
    type: str = Query("all", regex="^(all|users|anonim)$")
):
    session = SessionLocal()
    
    query = session.query(Post)
    
    if type == "users":
        query = query.filter(Post.user_id.isnot(None))
    elif type == "anonim":
        query = query.filter(Post.user_id.is_(None))
    
    if order == "asc":
        query = query.order_by(asc(Post.click_count))
    else:
        query = query.order_by(desc(Post.click_count))
    
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    
    def format_item(item):
        user_part = f"?u={item.user_id}" if item.user_id else ""
        return {
            "url": item.url,
            "custom_url": item.short_url,
            "share_url": f"http://localhost:{APP_EXTERNAL_PORT}/api/url/{item.short_url}{user_part}",
            "user_id": item.user_id,
            "counter": item.click_count
        }
    
    formatted_items = [format_item(item) for item in items]
    
    base_url = "http://localhost:{APP_EXTERNAL_PORT}/api/url-leaders"
    previous_offset = max(0, offset - limit)
    next_offset = offset + limit
    
    response = {
        "founded": total,
        "previous": f"{base_url}?limit={limit}&offset={previous_offset}&type={type}&order={order}" if offset > 0 else None,
        "next": f"{base_url}?limit={limit}&offset={next_offset}&type={type}&order={order}" if next_offset < total else None,
        "items": formatted_items
    }
    
    return response

@router.post("/generate-report/")
def generate_report(current_user: User = Depends(get_current_user)):
    try:
        send_user_report.delay(current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки письма на почту: {e}")

    return {"message": "Создание отчёта и его отправку поставлены в очередь. Спасибо, что выбрали наш сервис!"}