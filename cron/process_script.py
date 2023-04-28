import sys
from typing import Optional

from django.db import transaction

from const.script_job import ScriptJobStatus, ScriptJobType
from extensions.celery_app import CeleryApp
from extensions.oss import Oss
from models.bsgm import Bsgm, bsgm
from models.generate_recognition import (GenerateRecognition,
                                         generate_recognition)
from models.repair_image import RepairPortrait, repair_portrait
from models.tts import Tts, tts
from user.models import ScriptJob


@CeleryApp.task
def process_script():
    job: Optional[ScriptJob] = None
    with transaction.atomic():
        # 暂时只处理一条
        job = ScriptJob.objects.select_for_update().exclude(status=ScriptJobStatus.done).order_by("id asc").first()
        if not job or job.status == ScriptJobStatus.running:
            return

        job.status = ScriptJobStatus.running
        job.save()

    try:
        result = {}
        if job.type == ScriptJobType.tts:
            result = process_tts_job(job)
        elif job.type == ScriptJobType.bshm:
            result = process_bsgm_job(job)
        elif job.type == ScriptJobType.repair_portrait:
            result = process_repair_portrait_job(job)
        elif job.type == ScriptJobType.generate_recognition:
            result = process_generate_recognition_job(job)
        else:
            raise Exception("Unknown Job Type")

        job.status = ScriptJobStatus.done
        job.result = result # type: ignore
        job.save()

    except Exception as e:
        job.status = ScriptJobStatus.failed
        job.status_detail = f"Error: {e.__str__()}\n\n {sys.exc_info()}"
        job.save()


def process_tts_job(job: ScriptJob) -> dict:
    """Translate a text to a voice, then save to the oss"""
    tts_params = Tts.parse_raw(job.params)
    if not tts_params.text:
        raise Exception("tts text is Empty")

    with tts(tts_params.text, tts_params.voice) as data:
        oss_url = Oss.upload_data(data, f"/model-result/tts/{job.user_id}/{job.uuid}.wav")
        job.status = ScriptJobStatus.done
        result = {"url": oss_url} # type: ignore
        return result


def process_bsgm_job(job: ScriptJob) -> dict:
    """Pick a human from a image as a new image, then save to the oss"""
    bsgm_params = Bsgm.parse_raw(job.params)
    if not bsgm_params.file_url:
        raise Exception("file url is Empty")

    with bsgm(bsgm_params.file_url) as file:
        oss_url = Oss.upload_file(file, f"/model-result/bsgm/{job.user_id}/{job.uuid}.jpg")
        result = {"url": oss_url} # type: ignore
        return result


def process_repair_portrait_job(job: ScriptJob) -> dict:
    repair_portrait_params = RepairPortrait.parse_raw(job.params)
    if not repair_portrait_params.file_url:
        raise Exception("file url is Empty")

    with repair_portrait(repair_portrait_params.file_url) as file:
        oss_url = Oss.upload_file(file, f"/model-result/repair_portrait/{job.user_id}/{job.uuid}.jpg")
        result = {"url": oss_url} # type: ignore
        return result


def process_generate_recognition_job(job: ScriptJob) -> dict:
    generate_recognition_params = GenerateRecognition.parse_raw(job.params)
    if not generate_recognition_params.file_url:
        raise Exception("file url is Empty")
    return generate_recognition(file_path=generate_recognition_params.file_url)
