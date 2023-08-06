from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import recreationScrap, recreationMain
from .serializers import recreationMainSerializer, createRecreationSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class createRecreationView(APIView):
    # permission_classes = [IsAuthenticated]  # 인증된 사용자만 리뷰를 작성할 수 있도록 설정합니다.
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
                'photo': openapi.Schema(type=openapi.TYPE_FILE),
                'headCountMin': openapi.Schema(type=openapi.TYPE_INTEGER),
                'headCountMax': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['name', 'content', 'headCountMin', 'headCountMax'],
        )
    )
    def post(self, request, format=None):
        serializer = createRecreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class recreationMainView(generics.ListAPIView):
    serializer_class = recreationMainSerializer
    def get(self, request, format=None):
        recreations = recreationMain.objects.all()
        serializer = recreationMainSerializer(recreations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)