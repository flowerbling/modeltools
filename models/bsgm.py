"""
    人像抠图
"""
import os
import tempfile
from contextlib import contextmanager

import cv2
from modelscope.pipelines import pipeline
from pydantic import BaseModel

_TEST_IMAGE = "test_image.jpg"

class  Bsgm(BaseModel):
    file_url: str = ""



@contextmanager
def bsgm(file_path: str):
    """
        Args:
            file_path: str (文件的本地路径 测试阶段 暂时只支持本地文件)
    """
    p = pipeline('portrait-matting', 'damo/cv_unet_image-matting', device='cpu') # type: ignore
    generate_result = p(file_path)
    if not generate_result:
        raise Exception("process image failed")
    with tempfile.NamedTemporaryFile() as tmp:
        cv2.imwrite(tmp.name, generate_result['output_img'])  # type: ignore
        yield tmp.name


if __name__ == '__main__':
    bsgm(os.path.join(os.path.dirname(__file__), _TEST_IMAGE))
