"""
    图片人像修复
"""
import os
import tempfile
from contextlib import contextmanager

import cv2
from modelscope.pipelines import pipeline
from pydantic import BaseModel

_TEST_IMAGE = "test_image.jpg"

class RepairPortrait(BaseModel):
    file_url: str = ""



@contextmanager
def repair_portrait(file_path: str):
    """
        Args:
            file_path: str (文件的本地路径 测试阶段 暂时只支持本地文件)
    """

    p = pipeline('image-portrait-enhancement', 'damo/cv_gpen_image-portrait-enhancement')
    generate_result = p(file_path)
    if not generate_result:
        raise Exception("process image failed")
    with tempfile.NamedTemporaryFile() as tmp:
        cv2.imwrite(tmp.name, generate_result['output_img'])  # type: ignore
        yield tmp.name


if __name__ == '__main__':
    repair_portrait(os.path.join(os.path.dirname(__file__), _TEST_IMAGE))