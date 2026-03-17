# modeltools

[ModelScope Model Hub](https://modelscope.cn/models)
Take some interesting models from ModelScope for personal use. The task is designed as a queue-based system, as small, low-end servers cannot handle it.

Web creates tasks, the server starts Celery to consume tasks. You can start multiple consumers on multiple servers to process tasks.
You can use nohup to start cron-start.sh:

```shell
nohup sh cron-start.sh > cron.log 2>&1 &
```

## Environment Configuration

```shell
conda create -n modeltools
conda activate modelscope
# If you need to run Job
pip install torch torchvision torchaudio
pip install numpy==1.21.6
pip install tensorflow==1.15.0
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html # Environment for running model jobs, requires Linux

sh cron-start.sh

# Web environment
pip install -r web_requirements.txt

python manage.py runserver
```

## Already Added Models

```markdown
- Text to Speech
    Input: Text
    Output: Audio .wav
- Portrait Matting
    Input: Image
    Output: Image
- Portrait Enhancement
    Input: Image
    Output: Image
- General Object Detection
    Input: Image
    Output: Text, Score
```

## Web Preview

[Frontend GitHub Link](https://github.com/flowerbling/modeltools-frontend)