import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.settings import app_settings

def send_email(email:str, body:str, subject:str):
    with smtplib.SMTP_SSL('smtp.yandex.com') as server:
        server.login(app_settings.email_login, app_settings.email_pass)

        message = MIMEMultipart()
        message['From'] = app_settings.email_login
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server.send_message(message)