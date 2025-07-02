import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

app = Celery("ecommerce")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "send-cart-recovery-every-2-mins": {
        "task": "store.tasks.send_cart_recovery_emails",
        "schedule": 120.0,  # 2 minutes
    },
}
