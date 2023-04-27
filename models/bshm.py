"""
    人像抠图
"""
import os
import cv2
from modelscope.pipelines import pipeline


_TEST_IMAGE = "test_image.jpg"


def bsgm(file_path: str):
    """
        Args:
            file_path: str (文件的本地路径 测试阶段 暂时只支持本地文件)
    """
    p = pipeline('portrait-matting', 'damo/cv_unet_image-matting', device='cpu')
    generate_result = p(file_path)
    cv2.imwrite('_output_bshm.png', generate_result['output_img'])


bsgm(os.path.join(os.path.dirname(__file__), _TEST_IMAGE))
