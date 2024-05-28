import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from app.core.settings import EMAIL_USER, EMAIL_PASSWORD
from app.core.db import SessionLocal
from app.models.url_map import Post, User
import pandas as pd

def send_email(receiver_email: str, subject: str, body: str):
    with smtplib.SMTP_SSL('smtp.yandex.com') as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        message = MIMEMultipart()
        message['From'] = EMAIL_USER
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server.send_message(message)

def generate_user_report(user_id: int) -> str:
    session = SessionLocal()
    try:
        posts = session.query(Post).filter(Post.user_id == user_id).all()
        if not posts:
            print(f"URL ссылок не найдено для пользователя {user_id}")
            return None

        data = [{'short_url': post.short_url, 'original_url': post.url, 'click_count': post.click_count} for post in posts]

        df = pd.DataFrame(data)
        file_path = f'user_{user_id}_report.xlsx'
        df.to_excel(file_path, index=False)

        print(f"Report generated at {file_path}")
        return file_path
    finally:
        session.close()

def send_email_with_attachment(receiver_email: str, subject: str, body: str, attachment_path: str):
    message = MIMEMultipart()
    message['From'] = EMAIL_USER
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )
        message.attach(part)

    with smtplib.SMTP_SSL('smtp.yandex.com') as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, receiver_email, message.as_string())