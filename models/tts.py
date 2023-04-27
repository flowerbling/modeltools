from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys


def tts(text: str):
    model_id = 'damo/speech_sambert-hifigan_tts_zh-cn_16k'
    sambert_hifigan_tts = pipeline(task=Tasks.text_to_speech, model=model_id)
    output = sambert_hifigan_tts(input=text, voice='zhitian_emo')
    wav = output[OutputKeys.OUTPUT_WAV]
    with open('_output_tts.wav', 'wb') as f:
        f.write(wav)


print(tts("北京今天天气怎么样"))