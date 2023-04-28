from django.shortcuts import render
from user.models import User, ScriptJob
from user.serializers import UserSerializer,ScriptJobSerializer, parse_password
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework.request import Request
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

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ScriptJobAPI(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    queryset = ScriptJob.objects.all()
    serializer_class = ScriptJobSerializer
    lookup_field = 'uuid'

    def get_object(self):
        queryset = self.get_queryset()
        uuid = self.kwargs['uuid']
        obj = generics.get_object_or_404(queryset, uuid=uuid)
        return obj

    def get(self, request: Request, *args, **kwargs):
        uuid = request.query_params.get("uuid", "")
        if uuid:
            self.kwargs['uuid'] = uuid
            return self.retrieve(request, *args, **kwargs)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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