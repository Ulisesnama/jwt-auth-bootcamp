import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request


def jwt_auth_middleware(get_response):
    excluded_endpoints = ["/login/", "/token/refresh/"]

    def middleware(request: Request):
        if request.path in excluded_endpoints:
            return get_response(request)

        if "HTTP_AUTHORIZATION" in request.META:
            auth_header = request.META["HTTP_AUTHORIZATION"]
            try:
                _, token = auth_header.split()
                request.decoded_jwt = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                return get_response(request)
            except jwt.ExpiredSignatureError:
                return JsonResponse(
                    {
                        "status": "OK",
                        "data": "The token has expired. Please log in again to"
                        " obtain a new token.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            except jwt.InvalidTokenError:
                return JsonResponse(
                    {
                        "status": "OK",
                        "data": "The provided token is invalid. Please check "
                        "the token and try again.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return JsonResponse(
                {
                    "status": "OK",
                    "data": "An authentication token is required to access "
                    "this resource.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    return middleware
