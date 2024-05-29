import base64
import hashlib
from celery import Celery


app = Celery("tasks", broker="pyamqp://guest@localhost//")
EMAIL_SECRET="123"
def generate_email_verification_token(email: str) -> str:
    # Кодируем адрес электронной почты в base64
    email_baseencode = base64.urlsafe_b64encode(email.encode()).decode()
    # Формируем сигнатуру из адреса электронной почты и секретного ключа
    signature = hashlib.sha256(f"{email_baseencode}{EMAIL_SECRET}".encode()).hexdigest()
    # Формируем токен
    token = f"{email_baseencode}-{signature}"
    return token