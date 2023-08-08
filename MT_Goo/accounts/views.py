from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import DummySerializer
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # 회원가입은 인증 없이 접근해야 합니다.

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'token': openapi.Schema(type=openapi.TYPE_STRING)})},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)  # Token 객체의 objects 속성을 사용합니다.
        return Response({'token': token.key, 'name': user.name, 'email': user.email})

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DummySerializer
    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass

        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)