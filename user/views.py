import json
from uuid import uuid4

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from extensions.oss import Oss
from user.models import ScriptJob, User
from user.serializers import (ScriptJobSerializer, UserSerializer,
                              parse_password)
from utils.jwt_token import Token
from utils.pagination import Pagination


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
    pagination_class = Pagination
    lookup_field = 'uuid'


    def get_queryset(self):
        # 排序
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', None) # type: ignore
        if ordering is not None:
            return queryset.order_by(ordering)
        return queryset

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
        token = Token.from_jwt(request.headers['Authorization'])
        if not token:
            return Response({})
        queryset = self.get_queryset().filter(user_id=token.uid)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        user = User.objects.filter(username=username).first()
        if user and parse_password(password) == user.password:
            response["token"] = Token(username=username, uid=user.pk).to_jwt()
    return JsonResponse(response)



def upload(request):
    token = Token.from_jwt(request.headers['Authorization'])
    if not token:
        return Response({})

    if request.method == 'POST':
        if 'file' in request.FILES:
            # 获取上传的文件
            uploaded_file: InMemoryUploadedFile = request.FILES['file']
            file_type = request.POST.get('type')
            suffix = ''
            if file_type == 'image':
                suffix = '.jpg'

            oss_url = Oss.upload_data(uploaded_file.file, f'/uploads/{token.uid}/{uuid4().hex}{suffix}')
            return JsonResponse({'url': oss_url})
        else:
            return HttpResponseBadRequest('没有上传文件！')
    else:
        return HttpResponseBadRequest('不支持的请求方法！')