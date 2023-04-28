import os

from celery import Celery

_broker = os.environ.get("RedisQ")
_backend = os.environ.get("Redis")

celery_app = Celery("worker", backend=_backend, broker=_broker)
