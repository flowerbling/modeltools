# modeltools

[Modèle de la communauté ModelScope](https://modelscope.cn/models)
Extraction de modèles intéressants de la communauté ModelScope pour usage personnel. Les tâches sont organisées en file d'attente, car les petits serveurs peu puissants ne peuvent pas gérer cette charge.

Le Web crée des tâches, le serveur démarre Celery pour les consommer. Il est possible de démarrer plusieurs consommateurs sur plusieurs serveurs pour traiter les tâches.
Vous pouvez utiliser nohup pour démarrer cron-start.sh :
~~~shell
nohup sh cron-start.sh > cron.log 2>&1 &
~~~

## Configuration de l'environnement (Environnement de test)
~~~shell
conda create -n modeltools
conda activate modelscope
# Si vous avez besoin d'exécuter des Jobs
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
- Synthèse vocale (Texte vers audio)
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
[Lien GitHub du frontend](https://github.com/flowerbling/modeltools-frontend)
![Alt](images/home.png)
![Alt](images/new.png)
![Alt](images/tts.png)
![Alt](images/gen.png)
![Alt](images/pick.png)