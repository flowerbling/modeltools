# modeltools

[모두다 커뮤니티 모델 라이브러리](https://modelscope.cn/models)
모두다 커뮤니티에서 재미있는 모델들을 가져와서 직접 사용합니다. 작업을 큐 방식으로 만들면 작은 서버로도 감당할 수 있습니다.

Web에서 작업을 생성하고, 서버에서 Celery를 실행하여 작업을 소비합니다. 여러 서버에서 여러 워커를 실행하여 작업을 소비할 수 있습니다.
nohup을 사용하여 cron-start.sh를 시작할 수 있습니다.
~~~shell
nohup sh cron-start.sh > cron.log 2>&1 &
~~~
## 환경 설정
~~~shell
conda create -n modeltools
conda activate modelscope
# Job을 실행해야 하는 경우
pip install torch torchvision torchaudio
pip install numpy==1.21.6
pip install tensorflow==1.15.0
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html # 모델.job 실행 환경 - Linux 환경 필요

sh cron-start.sh

# Web 환경
pip install -r web_requirements.txt

python manage.py runserver
~~~

## 이미 추가된 모델
```markdown
- 텍스트를 음성으로 변환
	입력: 텍스트
	출력: 오디오 .wav
- 인물 배경제거
	입력: 이미지
	출력: 이미지
- 인물 이미지 보강
	입력: 이미지
	출력: 이미지
- 일반 물체 인식
	입력: 이미지
	출력: 텍스트, 점수
```

## Web 미리보기
[프론트엔드 Github 링크](https://github.com/flowerbling/modeltools-frontend)