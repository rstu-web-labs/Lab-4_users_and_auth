from celery import Celery

from app.celery.utils import SendMail
from app.core.settings import app_settings
from app.excel import set_exel_report

celery = Celery(__name__)
celery.conf.broker_url = app_settings.celery_broker_url
celery.conf.result_backend = app_settings.celery_result_backend

celery.autodiscover_tasks(packages=["app"])

send_mail_obj = SendMail()


@celery.task
def send_email(token_encrypt: str):
    message = f"http://localhost:8005/api/users/email-verification/{token_encrypt}"
    send_mail_obj.send_confirm(message, "Подтвердите почту")


@celery.task
def send_excel(email, user_all):
    name_file = set_exel_report(email, user_all)
    message = "Ваш отчет находится во вложении."
    subject = f"Выгрузка по пользователю {email}"
    send_mail_obj.send_excel(name_file, message, subject)
