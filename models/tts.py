from contextlib import contextmanager

from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from pydantic import BaseModel

MAX_TTS_TEXT_LENGTH = 1000

class Tts(BaseModel):
    text: str = ""


@contextmanager
def tts(text: str):
    if len(text) > MAX_TTS_TEXT_LENGTH:
        raise Exception(f"TTS 暂时只接受{MAX_TTS_TEXT_LENGTH}字以内的文本")

    model_id = 'damo/speech_sambert-hifigan_tts_zh-cn_16k'
    sambert_hifigan_tts = pipeline(task=Tasks.text_to_speech, model=model_id) # type: ignore
    output = sambert_hifigan_tts(input=text, voice='zhitian_emo')
    if output:
        raise Exception("TTS 生成失败")

    wav = output[OutputKeys.OUTPUT_WAV]
    with open('_output_tts.wav', 'wb') as f:
        f.write(wav)

        yield f



if __name__ == '__main__':
    text = "北京今天天气怎么样"
    with tts(text) as file:
        # process file file
        pass
