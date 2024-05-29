from celery import Celery
from app.core.utils import send_email
from app.core.security import generate_verification_token
from app.core.utils import send_email_with_attachment
from app.core.utils import generate_user_report
from app.core.db import SessionLocal
from app.models.url_map import User
from app.core.settings import SECRET_KEY, APP_EXTERNAL_PORT
import os
from app.core.celery_config import broker_url

celery_app = Celery("tasks", broker=broker_url)

@celery_app.task
def send_confirmation_email(email):
    verification_token = generate_verification_token(email, SECRET_KEY)
    verification_link = f"http://localhost:{APP_EXTERNAL_PORT}/api/users/email-verification/{verification_token}"
    email_subject = "Подтверждение адреса электронной почты"
    email_body = f"Для подтверждения адреса электронной почты перейдите по ссылке: {verification_link}"
    send_email(email, email_subject, email_body)

@celery_app.task
def send_user_report(user_id: int):
    file_path = generate_user_report(user_id)
    
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    
    send_email_with_attachment(
        receiver_email=user.email,
        subject="Отчёт по URL",
        body="Вот ваш отчёт по URL ссылкам.",
        attachment_path=file_path
    )
    
    os.remove(file_path)