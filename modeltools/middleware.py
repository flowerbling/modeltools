from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, JsonResponse)

from modeltools import settings
from utils.error import Error400
from utils.jwt_token import Token


class HandleOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request)
        import sys

        sys.stdout.write(request.__str__())
        sys.stdout.flush()
        if request.method == 'OPTIONS':
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'
            print(request)
            return response
        else:
            response = self.get_response(request)
            return response


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Error400):
            # 处理自定义异常
            return JsonResponse({'msg': exception.message, "code": 1}, status=400)
        else:
            error_str = ""
            print(exception)
            if hasattr(exception, 'message'):
                error_str = getattr(exception, 'message')
            else:
                error_str = str(exception)
            return JsonResponse({"msg": error_str, "code": 1}, status=500)            # 处理其他异常
            # return JsonResponse({"msg": "服务器开小差了~~~", "code": 1}, status=500)


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.path_info in settings.NO_AUTH_ROUTERS:
                return self.get_response(request)
        except Exception as e:
            print(e)
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return HttpResponseBadRequest("Authorization header missing")

        try:
            token = Token.from_jwt(auth_header)
            if not token:
                return HttpResponseForbidden("Invalid or expired JWT token")
        except IndexError:
            return HttpResponseBadRequest("Token not provided")
        except Exception:
            return HttpResponseForbidden("Invalid JWT token")

        return self.get_response(request)