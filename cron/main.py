
from extensions.celery.celery_app import celery_app

celery_app.conf.beat_schedule = {
#     'name': {
#         'task': func.name,
#         'schedule': timedelta(seconds=3),
#     }
}