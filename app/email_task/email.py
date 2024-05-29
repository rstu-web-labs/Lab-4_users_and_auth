import cowsay
import smtplib
import pandas as pd
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import Depends
from sqlalchemy import select

from app.core.db import get_session, Session
from app.core.settings import app_settings
from app.models.user_map import UserModel
from app.models.url_map import ShortUrl


def send_email(email:str, body:str, subject:str):
    with smtplib.SMTP_SSL('smtp.yandex.com') as server:
        server.login(app_settings.email_login, app_settings.email_pass)

        message = MIMEMultipart()
        message['From'] = app_settings.email_login
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(cowsay.get_output_string('pig', body), 'plain'))

        server.send_message(message)

def send_report(email:str, subject:str):
    path = generate_report(email)
    with smtplib.SMTP_SSL('smtp.yandex.com') as server:
        server.login(app_settings.email_login, app_settings.email_pass)

        message = MIMEMultipart()
        message['From'] = app_settings.email_login
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(cowsay.get_output_string('cow','Отчет по ссылкам!'), 'plain'))

        with open(path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(path)}",
            )
            message.attach(part)

        server.send_message(message)  
    os.remove(path)  

def generate_report(email):
    with get_session().__next__() as session:
        posts = session.execute(select(ShortUrl).where(ShortUrl.user_id == (select(UserModel.id).where(UserModel.email == email)))).scalars().all()
    data = [{'short_url': post.short_url, 'original_url': post.url, 'redirect_count': post.redirect_count} for post in posts]
    df = pd.DataFrame(data)
    file_path = f'_report.xlsx'
    df.to_excel(file_path, index=False)
    return file_path

