from app.core.settings import CELERY_USER, CELERY_PASSWORD,BROKER_HOST, BROKER_PORT

broker_url = f"amqp://{CELERY_USER}:{CELERY_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/"
result_backend = 'rpc://'
CELERY_TASK_IGNORE_RESULT = True