# modeltools

[مكتبة نماذج MindSpore](https://modelscope.cn/models)
احصل على بعض النماذج المثيرة للاهتمام من مجتمع MindSpore لاستخدامك الشخصي. المهمة مصممة على شكل قائمة انتظار، والخادم الصغير لا يتحمل ذلك.

إنشاء مهمة ويب، بدء الخادم لـ Celery للاستهلاك، يمكن تشغيل عدة مستهلكين على خوادم متعددة لاستهلاك المهام
يمكنك استخدام noohup لبدء cron-start.sh
~~~shell
nohup sh cron-start.sh > cron.log 2>&1 &
~~~
## تكوين البيئة
~~~shell
conda create -n modeltools
conda activate modelscope
# إذا كنت بحاجة إلى تشغيل Job
pip install torch torchvision torchaudio
pip install numpy==1.21.6
pip install tensorflow==1.15.0
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html # بيئة تشغيل نموذج الوظيفة تحتاج إلى بيئة لينكس

sh cron-start.sh

# بيئة الويب
pip install -r web_requirements.txt

python manage.py runserver
~~~

## النماذج المضافة
```markdown
- تحويل النص إلى كلام
	إدخال نص
	إخراج صوت .wav
- إزالة خلفية الصورة الشخصية
	إدخال صورة
	إخراج صورة
- تعزيز الصورة الشخصية
	إدخال صورة
	إخراج صورة
- التعرف على الكائنات العامة
	إدخال صورة
	إخراج نص، درجة
```

## معاينة الويب
[رابط GitHub للواجهة الأمامية](https://github.com/flowerbling/modeltools-frontend)
![Alt](images/home.png)
![Alt](images/new.png)
![Alt](images/tts.png)
![Alt](images/gen.png)
![Alt](images/pick.png)