from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    task_routes={
        "tasks.celery_tasks.send_email_task": {"queue": "email_queue"}
    }
)
