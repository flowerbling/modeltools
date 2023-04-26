from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import modelscope.models.audio.tts.sambert_hifi
def tts(text: str):
    p = pipeline('text-to-speech', 'damo/speech_sambert-hifigan_tts_zh-cn_16k', device='cpu')
    print(p(text))

# tts("北京今天天气怎么样")