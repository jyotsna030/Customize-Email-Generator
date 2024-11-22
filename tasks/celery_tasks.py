from celery_config import celery_app
from app.email_utils import send_email_smtp

@celery_app.task
def send_email_task(recipient, subject, body, smtp_server, smtp_port, email, password):
    send_email_smtp(recipient, subject, body, smtp_server, smtp_port, email, password)
