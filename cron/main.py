
from datetime import timedelta

from extensions.celery_app import CeleryApp

from .process_script import process_script

CeleryApp.conf.beat_schedule = {
    'name': {
        'process_script': process_script.name,
        'schedule': timedelta(seconds=3),
    }
}