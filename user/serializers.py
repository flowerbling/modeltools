from datetime import datetime
from hashlib import md5
from uuid import uuid4

from rest_framework import serializers

from user.models import ScriptJob, User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(style={'base_template': 'textarea.html'})
    password = serializers.CharField(required=False, allow_blank=True, max_length=200)

    def create(self, validated_data):
        username = validated_data.get("username")
        if 5 > len(username) or len(username) > 18:
            raise Exception("username not valid")
        validated_data["password"] = parse_password(validated_data.get("password", ""))
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.password = parse_password(validated_data.get('username', instance.username))
        instance.save()
        return instance


class ScriptJobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    uuid = serializers.UUIDField(default=uuid4().hex)
    user_id = serializers.IntegerField(default=0)
    type = serializers.CharField(default="", max_length=255)
    params = serializers.JSONField(default={})
    result = serializers.JSONField(default={})
    status = serializers.CharField(default='pending', max_length=255)
    status_detail = serializers.CharField(default=None)
    created_at = serializers.DateTimeField(default=datetime.now())

    def create(self, validated_data):
        validated_data["uuid"] = uuid4().hex

        return ScriptJob.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance

def parse_password(input: str) -> str:
    if len(input) != 32:
        raise Exception("password not valid")

    return md5(input.encode('utf-8')).hexdigest() # type: ignore
