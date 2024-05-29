from celery import Celery
from app.core.celery_config import broker_url

celery_app = Celery('tasks', broker=broker_url)

if __name__ == '__main__':
    celery_app.start()