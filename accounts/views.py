import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RefreshTokenSerializer
from .utils import generate_jwt_tokens


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                access_token, refresh_token = generate_jwt_tokens(user)
                return Response(
                    {
                        "status": "OK",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "status": "UNAUTHORIZED",
                    "data": "The username or password you are trying to log in"
                    " with are incorrect.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {"status": "BAD_REQUEST", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RefreshTokenView(APIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request: Request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data["refresh_token"]
            try:
                payload = jwt.decode(
                    refresh_token,
                    f"refresh.{settings.SECRET_KEY}",
                    algorithms=["HS256"],
                )
                username = payload["username"]
                user = User.objects.get_by_natural_key(username)
                if user is not None:
                    access_token, refresh_token = generate_jwt_tokens(user)
                    return Response(
                        {
                            "status": "OK",
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                        },
                        status=status.HTTP_200_OK,
                    )
            except jwt.ExpiredSignatureError:
                return Response(
                    {
                        "status": "OK",
                        "data": "The token has expired. Please log in again to"
                        " obtain a new token.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            except jwt.InvalidTokenError:
                return Response(
                    {
                        "status": "OK",
                        "data": "The provided token is invalid. Please check "
                        "the token and try again.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(
            {"status": "BAD_REQUEST", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
