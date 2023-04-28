from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class User(models.Model):
    username = models.CharField(max_length=16, blank=True, null=False)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ScriptJob(models.Model):
    uuid = models.UUIDField(unique=True)
    user_id = models.IntegerField(null=False, default=0)
    type = models.CharField(null=False, default="", max_length=255)
    params = models.JSONField(null=False, default=dict)
    status = models.CharField(default='pending', null=False, max_length=255)
    status_detail = models.TextField(default=None, null=True)
    result = models.JSONField(null=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
