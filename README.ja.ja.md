# modeltools

[魔搭社区モデルライブラリ](https://modelscope.cn/models)
魔搭コミュニティから интересные モデルを引っ張って自分で使う。タスクはキュー式にして、小規模なサーバーでは対応できない。

Webでタスクを作成、サーバーがCeleryを起動してコンシューマーがタスクを消費、複数のサーバーで複数のコンシューマーを起動してタスクを消費できる
nohup で cron-start.sh を起動可能
~~~shell
nohup sh cron-start.sh > cron.log 2>&1 &
~~~
## 環境設定
~~~shell
conda create -n modeltools
conda activate modelscope
# Jobを実行する必要がある場合
pip install torch torchvision torchaudio
pip install numpy==1.21.6
pip install tensorflow==1.15.0
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html # モデルjobの環境 Linux環境が必要

sh cron-start.sh

# Web環境
pip install -r web_requirements.txt

python manage.py runserver
~~~

## 追加済みモデル
```markdown
- テキストから音声へ
	入力 テキスト
	出力 音声 .wav
- 人物切り抜き
	入力 画像
	出力 画像
- 人物強調
	入力 画像
	出力 画像
- 一般物体認識
	入力 画像
	出力 テキスト、スコア
```

## Webプレビュー
[フロントエンドGithubリンク](https://github.com/flowerbling/modeltools-frontend)