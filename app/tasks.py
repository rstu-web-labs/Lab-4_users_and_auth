from app.celery import app
from app.models.user import User
from app.schemas.url import get_db
import base64
import hmac
import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
SECRET_KEY = "mysecretkey"


EMAIL_FROM = "noreply@example.com"
EMAIL_SUBJECT = "Email Verification"
EMAIL_BODY_TEMPLATE = """
<p>Thank you for registering!</p>
<p>Please click the following link to verify your email:</p>
<p><a href="{verification_url}">Verify Email</a></p>
"""

SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 587
SMTP_USERNAME = "task3qwerty12345"
SMTP_PASSWORD = "hpkiemyxwcbygxgl"

@app.task
def send_email_verification(email: str, verification_token: str):
    # Генерируем URL для подтверждения адреса электронной почты
    verification_url = f"http://localhost/api/users/email-verification/{verification_token}"
    
    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = EMAIL_SUBJECT

    # Заполняем тело сообщения
    email_body = EMAIL_BODY_TEMPLATE.format(verification_url=verification_url)
    msg.attach(MIMEText(email_body, 'html'))

    # Подключаемся к SMTP-серверу и отправляем сообщение
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())