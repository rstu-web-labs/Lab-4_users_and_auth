from celery import Celery
from app.core.utils import send_email
from app.core.security import generate_verification_token
from app.core.utils import send_email_with_attachment
from app.core.utils import generate_user_report
from app.core.db import SessionLocal
from app.models.url_map import User
import os

celery_app = Celery("tasks", broker="amqp://guest:guest@localhost:5672/")

@celery_app.task
def send_confirmation_email(email):
    secret_key = "secretkey"
    verification_token = generate_verification_token(email, secret_key)
    verification_link = f"http://localhost/api/users/email-verification/{verification_token}"
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