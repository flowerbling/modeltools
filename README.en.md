# modeltools

[ModelScope Model Library](https://modelscope.cn/models)
Get some interesting models from ModelScope for personal use. Tasks are implemented in a queue pattern, as small servers cannot handle the load.

Web creates tasks, the server starts Celery for consumption, and multiple consumers can be started on multiple servers to process tasks.
You can use nohup to start cron-start.sh:
```shell
nohup sh cron-start.sh > cron.log 2>&1 &
```

## Environment Setup
```shell
conda create -n modeltools
conda activate modelscope
# If you need to run Jobs
pip install torch torchvision torchaudio
pip install numpy==1.21.6
pip install tensorflow==1.15.0
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html # Environment for running model jobs, requires Linux

sh cron-start.sh

# Web environment
pip install -r web_requirements.txt

python manage.py runserver
```

## Models Added
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
- General Object Recognition
    Input: Image
    Output: Text, Score
```

## Web Preview
[Frontend GitHub Link](https://github.com/flowerbling/modeltools-frontend)
![Alt](images/home.png)
![Alt](images/new.png)
![Alt](images/tts.png)
![Alt](images/gen.png)
![Alt](images/pick.png)