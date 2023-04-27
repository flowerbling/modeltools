from django.shortcuts import render
from user.models import User
from user.serializers import UserSerializer, parse_password
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework import mixins, generics
from django.core.handlers.wsgi import WSGIRequest
import json
from utils.jwt_token import Token

class UserAPI(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



def login(request: WSGIRequest):
    response = {"token": ""}
    request_body: dict = json.loads(request.body)
    username = request_body.get("username")
    password = request_body.get("password")
    if username and password:
        user = User.objects.get(username=username)
        if user and parse_password(password) == user.password:
            response["token"] = Token(username=username).to_jwt()

    return JsonResponse(response)