
from extensions.celery_app import CeleryApp

CeleryApp.conf.beat_schedule = {
#     'name': {
#         'task': func.name,
#         'schedule': timedelta(seconds=3),
#     }
}