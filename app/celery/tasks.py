from celery import Celery
import secrets
from time import sleep

from app.core.config import get_settings

celery_app = Celery(
    "tasks",
    broker=get_settings().CELERY_BROKER_URL,
    backend=get_settings().CELERY_RESULT_BACKEND,
)


@celery_app.task
def send_email_notification(task_title: str):
    secure_random_int = secrets.randbelow(10)  # Mock for sending email notification
    sleep(secure_random_int)
    print(f"Email Notification Sended for {task_title}")
