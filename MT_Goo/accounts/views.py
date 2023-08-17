from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .models import CustomUser, suggestion
from .serializers import CustomUserSerializer, LoginSerializer, suggestionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import DummySerializer
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # 회원가입은 인증 없이 접근해야 합니다.


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_update(self, serializer):
        if 'password' in self.request.data:
            new_password = self.request.data.get('password')
            # 비밀번호를 해싱하여 저장하는 대신, set_password() 메서드 사용
            serializer.instance.set_password(new_password)
        serializer.save()

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                      'token': openapi.Schema(type=openapi.TYPE_STRING)})},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # 기존 토큰 삭제
        try:
            old_token = Token.objects.get(user=user)
            old_token.delete()
        except Token.DoesNotExist:
            pass

        # 새로운 토큰 생성
        token = Token.objects.create(user=user)

        response_data = {
            'token': token.key,
            'name': user.name,
            'email': user.email,
            'pk': user.pk,
        }


        # is_staff 값이 True인 경우에도 isStaff 정보를 응답에 추가
        response_data['isStaff'] = user.is_staff

        return Response(response_data)


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


class suggestionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['content'],
        ),
        responses={
            status.HTTP_201_CREATED: suggestionSerializer(),
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def post(self, request):
        serializer = suggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Note the change here
        return Response(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: suggestionSerializer(many=True)}
    )
    def get(self, request):
        suggestions = suggestion.objects.all()
        serializer = suggestionSerializer(suggestions, many=True)
        return Response(serializer.data)