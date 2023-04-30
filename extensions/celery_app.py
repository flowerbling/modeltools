import os
from manage import init
from celery import Celery
from datetime import timedelta
import django
init()
django.setup()

_broker = os.environ.get("RedisQ")
_backend = os.environ.get("Redis")
celery_app = Celery("worker", backend=_backend, broker=_broker)
celery_app.conf.beat_schedule = {
    'process_script': {
        'task': 'cron.process_script.process_script',
        'schedule': timedelta(seconds=3),
    }
}