from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import recreationScrap, recreationMain
from .serializers import recreationMainSerializer, createRecreationSerializer, recreationScrapSerializer, recreationDetailSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from accounts.models import CustomUser
from drf_yasg.openapi import Response as OpenApiResponse
from rest_framework.pagination import PageNumberPagination


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


class recreationMainView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY,
                          description="Page number", type=openapi.TYPE_INTEGER),
    ],
        responses={status.HTTP_200_OK: recreationMainSerializer(many=True)})
    def get(self, request, format=None):
        recreations = recreationMain.objects.all()
        paginator = PageNumberPagination()
        paginated_lodgings = paginator.paginate_queryset(recreations, request)
        serializer = recreationMainSerializer(
            paginated_lodgings, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)


class recreationDetailView(APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: recreationDetailSerializer})
    def get(self, request, pk, format=None):
        try:
            recreation = recreationMain.objects.get(pk=pk)
            serializer = recreationDetailSerializer(
                instance=recreation, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except recreationMain.DoesNotExist:
            return Response({"error": "recreation not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=createRecreationSerializer,
        responses={
            status.HTTP_200_OK: createRecreationSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request')
        }
    )
    def put(self, request, pk, format=None):
        recreation = recreationMain.objects.get(pk=pk)
        serializer = createRecreationSerializer(recreation, data=request.data)
        if serializer.is_valid():
            recreation = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description='No content'),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description='Not found')
        }
    )
    def delete(self, request, pk, format=None):
        recreation = recreationMain.objects.get(pk=pk)
        recreation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class recreationScrapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'recreationPk': openapi.Schema(type=openapi.TYPE_INTEGER),
                'isScrap': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
            required=['recreationPk', 'isScrap'],
        )
    )
    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id
        recreationPk = data.get('recreationPk')
        # lodging과 user가 같은 객체가 존재한다면 업데이트(덮어 쓰기)
        scrap, created = recreationScrap.objects.update_or_create(
            recreation=recreationMain.objects.get(pk=recreationPk),
            user=CustomUser.objects.get(pk=request.user.id),
            defaults={'isScrap': data.get('isScrap')}
        )

        serializer = recreationScrapSerializer(scrap)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class myPageRecreationScrapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: recreationMainSerializer(many=True)})
    def get(self, request, format=None):
        user = request.user
        scraps = recreationScrap.objects.filter(user=user, isScrap=True)
        recreations = []
        for scrap in scraps:
            recreations.append(
                recreationMain.objects.get(pk=scrap.recreation.pk))
        serializer = recreationMainSerializer(
            recreations, many=True, context={'request': request})
        return Response(serializer.data)
