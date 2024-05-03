from celery import Celery

from app.core.settings import app_settings
from app.email_task.email import send_email

celery = Celery(broker=app_settings.rabbit_url)

@celery.task
def send_email_task(email:str, body:str, subject:str = 'Подтверждение почты'):
    send_email(email, body, subject)