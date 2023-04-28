"""
    图片人像修复
"""
import os

from modelscope.pipelines import pipeline
from pydantic import BaseModel

_TEST_IMAGE = "test_image.jpg"

class GenerateRecognition(BaseModel):
    file_url: str = ""


def generate_recognition(file_path: str) -> dict:
    """
        Args:
            file_path: str (文件的本地路径 测试阶段 暂时只支持本地文件)
    """

    p = pipeline('general-recognition', 'damo/cv_resnest101_general_recognition')
    generate_result = p(file_path)
    if not generate_result:
        raise Exception("process image failed")

    return generate_result  # type: ignore


if __name__ == '__main__':
    generate_recognition(os.path.join(os.path.dirname(__file__), _TEST_IMAGE))