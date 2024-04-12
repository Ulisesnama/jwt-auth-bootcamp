from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserSerializer
from .utils import generate_jwt_token


class UserViews(APIView):
    serializer_class = UserSerializer

    def get(self, request: Request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(
            {"status": "OK", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "CREATED", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "BAD_REQUEST", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDetailViews(APIView):
    serializer_class = UserSerializer

    def get(self, request: Request, username: str):
        user = User.objects.get_by_natural_key(username)
        serializer = UserSerializer(user)
        return Response(
            {"status": "OK", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request, username: str):
        user = User.objects.get_by_natural_key(username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "OK", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "BAD_REQUEST", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request: Request, username: str):
        user = User.objects.get_by_natural_key(username)
        user.delete()
        return Response(
            {"status": "OK", "data": "User deleted."},
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = generate_jwt_token(user)
                return Response(
                    {"status": "OK", "access_token": token},
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
