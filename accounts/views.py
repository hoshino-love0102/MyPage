from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from datetime import timedelta

from .serializers import SignupSerializer, LoginSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = Response({
            "message": "회원가입 성공",
            "access": access,
        }, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            expires=now() + timedelta(days=7)
        )

        return response


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = Response({
            "message": "로그인 성공",
            "access": access,
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            expires=now() + timedelta(days=7)
        )

        return response
