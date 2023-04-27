from rest_framework import serializers
from user.models import User, LANGUAGE_CHOICES, STYLE_CHOICES
from hashlib import md5


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(style={'base_template': 'textarea.html'})
    password = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        username = validated_data.get("username")
        if 5 < len(username) or len(username) > 18:
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


def parse_password(input: str) -> str:
    if len(input) < 5 or len(input) > 18:
        raise Exception("password not valid")

    return md5(input.encode('utf-8')).hexdigest()

