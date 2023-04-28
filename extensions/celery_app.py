import os

from celery import Celery

_env: dict = os.environ  # type: ignore
_broker = _env.get("RedisQ")
_backend = _env.get("Redis")

CeleryApp = Celery("worker", backend=_backend, broker=_broker)
CeleryApp = Celery("worker", backend=_backend, broker=_broker)
