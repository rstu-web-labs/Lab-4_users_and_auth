import base64
from datetime import date
import hmac
from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
import hashlib
from app.celery import generate_email_verification_token
from app.schemas.url import URLCreate, Urls, get_db, generate_short_url
from app.schemas.user import UserCreate, UserResponse
from app.models.url_map import UrlMap
from app.models.user import User
from app.tasks import send_email_verification, SECRET_KEY


router = APIRouter()

# Эндпоинт для создания короткого URL
@router.post("/url/", response_model=Urls)
async def create_url(url_in: URLCreate, db: Session = Depends(get_db)):
    short_url = url_in.short_url or generate_short_url()
    while db.query(UrlMap).filter(UrlMap.short_url == short_url).first():
        short_url = generate_short_url()

    url = UrlMap(short_url=short_url, url=url_in.original_url, created_at=date.today())

    try:
        stmt = insert(UrlMap).values(url=url_in.original_url, short_url=short_url, created_at=date.today())
        db.execute(stmt)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create URL")

    return {"url": url.url, "short_url": url.short_url}

# Эндпоинт для получения оригинального URL по короткому URL
@router.get("/url/{short_url}/", summary="Get Url")
def get_url(short_url: str, db: Session = Depends(get_db)):
    url_map = db.query(UrlMap).filter(UrlMap.short_url == short_url).first()
    if not url_map:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url_map.url)

@router.post("/users/register/", response_model=UserResponse)
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Валидация пароля
    try:
        UserCreate.password_validation(user_in.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Хеширование пароля
    hashed_password = hashlib.sha256(user_in.password.encode()).hexdigest()
    
    # Генерация токена для подтверждения адреса электронной почты
    email_verification_token = generate_email_verification_token(user_in.email)
    
    user = User(email=user_in.email, hashed_password=hashed_password, email_verification_token=email_verification_token)
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Запуск отложенной задачи Celery для отправки электронной почты с токеном
    send_email_verification.delay(user_in.email, email_verification_token)

    return {"email": user.email, "message": "Please confirm your email to complete registration"}

@router.get("/users/email-verification/{verify_token}/", summary="Verify Email")
def verify_email(verify_token: str, db: Session = Depends(get_db)):
    email, signature = verify_token.split('-')
    email = base64.b64decode(email).decode('utf-8')
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not hmac.new(SECRET_KEY.encode(), msg=email.encode(), digestmod=hashlib.sha256).hexdigest() == signature:
        raise HTTPException(status_code=400, detail="Invalid signature")
    user.email_verified = True
    db.commit()
    return {"email": user.email, "message": "Email verified"}
