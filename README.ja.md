# modeltools

[魔搭社区モデルライブラリ](https://modelscope.cn/models)
魔搭社区から面白いモデルを自由に引っ張って使えます。タスクをキューイング方式にして、小規模なサーバーでは対応しきれない問題を解決します。

Webでタスクを作成し、サーバーでCeleryがコンシューマとして処理、複数のサーバーで複数のコンシューマを起動してタスクを処理できます
nohupでcron-start.shを起動できます
~~~shell
nohup sh cron-start.sh > cron.log 2>&1 &
~~~
## 環境設定（テスト環境）
~~~shell
conda create -n modeltools
conda activate modelscope
# Jobを実行する必要がある場合
pip install torch torchvision torchaudio
pip install numpy==1.21.6
pip install tensorflow==1.15.0
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html # モデルJobを実行するための環境。Linux環境が必要

sh cron-start.sh

# Web環境
pip install -r web_requirements.txt

python manage.py runserver
~~~

## 追加済みのモデル
```markdown
- テキスト読み上げ（Text-to-Speech）
	入力：テキスト
	出力：音声 .wav
- ポートレート切り抜き
	入力：画像
	出力：画像
- ポートレート強調
	入力：画像
	出力：画像
- 一般物体認識
	入力：画像
	出力：テキスト、スコア
```

## Webプレビュー
[フロントエンドGitHubリンク](https://github.com/flowerbling/modeltools-frontend)
![Alt](images/home.png)
![Alt](images/new.png)
![Alt](images/tts.png)
![Alt](images/gen.png)
![Alt](images/pick.png)