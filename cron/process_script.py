import sys
from typing import Optional

from django.db import transaction

from const.script_job import ScriptJobStatus, ScriptJobType
from extensions.celery_app import CeleryApp
from extensions.oss import Oss
from models.bsgm import Bsgm, bsgm
from models.tts import Tts, tts
from user.models import ScriptJob


@CeleryApp.task
def process_script():
	job: Optional[ScriptJob] = None
	with transaction.atomic():
		job = ScriptJob.objects.select_for_update().filter(status=ScriptJobStatus.pending).first()
		if not job:
			return

		job.status = 'running'
		job.save()

	try:
		if job.type == ScriptJobType.tts:
			process_tts_job(job)
		elif job.type == ScriptJobType.bshm:
			process_bsgm_job(job)
		else:
			raise Exception("Unknown Job Type")
	except Exception as e:
		job.status = ScriptJobStatus.failed
		job.status_detail = f"Error: {e.__str__()}\n\n {sys.exc_info()}"
		job.save()


def process_tts_job(job: ScriptJob):
	"""Translate a text to a voice, then save to the oss"""
	tts_params = Tts.parse_raw(job.params)
	if not tts_params.text:
		raise Exception("tts text is Empty")

	with tts(tts_params.text) as data:
		oss_url = Oss.upload_data(data, f"/model-result/tts/{job.user_id}/{job.uuid}.wav")
		job.status = ScriptJobStatus.done
		job.result = {"url": oss_url} # type: ignore
		job.save()

def process_bsgm_job(job: ScriptJob):
	"""Pick a human from a image as a new image, then save to the oss"""
	bsgm_params = Bsgm.parse_raw(job.params)
	if not bsgm_params.file_url:
		raise Exception("file url is Empty")

	with bsgm(bsgm_params.file_url) as file:
		oss_url = Oss.upload_file(file, f"/model-result/bsgm/{job.user_id}/{job.uuid}.jpg")
		job.status = ScriptJobStatus.done
		job.result = {"url": oss_url} # type: ignore
		job.save()