# modeltools

[Modèle de la communauté魔搭](https://modelscope.cn/models)
Obtenez des modèles intéressants de la communauté 模型魔搭pour votre propre utilisation. Les tâches sont organisées en file d'attente, car les petits serveurs低配置 ne peuvent pas supporter cela.

Web crée la tâche, le serveur démarre Celery pour consommation, et peut démarrer plusieurs consommateurs sur plusieurs serveurs pour consommer les tâches
Vous pouvez utiliser nohup pour démarrer cron-start.sh
~~~shell
nohup sh cron-start.sh > cron.log 2>&1 &
~~~
## Configuration de l'environnement
~~~shell
conda create -n modeltools
conda activate modelscope
# Si vous avez besoin d'exécuter Job
pip install torch torchvision torchaudio
pip install numpy==1.21.6
pip install tensorflow==1.15.0
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html # Environnement pour exécuter les jobs de modèle, nécessite un environnement Linux

sh cron-start.sh

# Environnement Web
pip install -r web_requirements.txt

python manage.py runserver
~~~

## Modèles déjà ajoutés
```markdown
- Synthèse vocale (texte vers audio)
	Entrée : Texte
	Sortie : Audio .wav
- Segmentation de portrait
	Entrée : Image
	Sortie : Image
- Amélioration de portrait
	Entrée : Image
	Sortie : Image
- Reconnaissance d'objets通用
	Entrée : Image
	Sortie : Texte, Score
```

## Aperçu Web
[Lien GitHub前端](https://github.com/flowerbling/modeltools-frontend)