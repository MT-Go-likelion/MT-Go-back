from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import lodgingMain, lodgingPhoto, review, lodgingScrap
from .serializers import lodgingCreateSerializer, lodgingMainSerializer, lodgingDetailSerializer, reviewCreateSerializer, reviewSerializer, lodgingScrapSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from django.core.serializers import serialize
from drf_yasg.openapi import Response as OpenApiResponse
from MT_Goo.pagination import lodingListPagination, reviewListPagination
from django.db.models import Count
from django.db.models import Count, Q

class createLodgingView(APIView):
    @swagger_auto_schema(request_body=lodgingCreateSerializer)
    def post(self, request, format=None):
        serializer = lodgingCreateSerializer(data=request.data)
        if serializer.is_valid():
            lodging = serializer.save()
            if request.FILES.getlist('photos'):
                photos = request.FILES.getlist('photos')
                for photo in photos:
                    lodgingPhoto.objects.create(lodging=lodging, image=photo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class lodgingMainView(APIView):
    serializer_class = lodgingMainSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('place', openapi.IN_QUERY,
                              description="Place name for lodging search", type=openapi.TYPE_STRING),
            openapi.Parameter('minheadCount', openapi.IN_QUERY,
                              description="Minimum head count for lodging search", type=openapi.TYPE_INTEGER),
            openapi.Parameter('maxheadCount', openapi.IN_QUERY,
                              description="Maximum head count for lodging search", type=openapi.TYPE_INTEGER),
            openapi.Parameter('minlowWeekdayPrice', openapi.IN_QUERY,
                              description="Minimum low weekday price for lodging search", type=openapi.TYPE_INTEGER),
            openapi.Parameter('maxlowWeekdayPrice', openapi.IN_QUERY,
                              description="Maximum low weekday price for lodging search", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY,
                              description="Page number", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: lodgingMainSerializer(many=True),
        }
    )
    def get(self, request, format=None):
        lodgings = lodgingMain.objects.all()

        place = request.query_params.get('place')
        if place:
            lodgings = lodgings.filter(place__icontains=place)
        
        min_headCount = request.query_params.get('minheadCount')
        max_headCount = request.query_params.get('maxheadCount')
        if min_headCount and max_headCount:
            lodgings = lodgings.filter(headCount__gte=int(min_headCount), headCount__lte=int(max_headCount))
    
        min_lowWeekdayPrice = request.query_params.get('minlowWeekdayPrice')
        max_lowWeekdayPrice = request.query_params.get('maxlowWeekdayPrice')
        if max_lowWeekdayPrice and max_lowWeekdayPrice:
            lodgings = lodgings.filter(lowWeekdayPrice__gte=int(min_lowWeekdayPrice), lowWeekdayPrice__lte=int(max_lowWeekdayPrice))

        paginator = lodingListPagination()
        paginated_lodgings = paginator.paginate_queryset(lodgings, request)

        serializer = lodgingMainSerializer(
            paginated_lodgings, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class lodgingDetailView(APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: lodgingDetailSerializer})
    def get(self, request, pk, format=None):
        try:
            lodging = lodgingMain.objects.get(pk=pk)
            serializer = lodgingDetailSerializer(
                lodging, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except lodgingMain.DoesNotExist:
            return Response({"error": "Lodging not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=lodgingCreateSerializer,
        manual_parameters=[
            openapi.Parameter('deleteImage', openapi.IN_QUERY, description="List of image Pk to delete",
                              type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
        ],
        responses={
            status.HTTP_200_OK: lodgingCreateSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request')
        }
    )
    def put(self, request, pk, format=None):
        lodging = lodgingMain.objects.get(pk=pk)
        serializer = lodgingCreateSerializer(lodging, data=request.data)
        if serializer.is_valid():
            lodging = serializer.save()
            if request.data.getlist('deleteImage'):
                delImagePkList = request.data.getlist('deleteImage')
                for pk in delImagePkList:
                    if lodgingPhoto.objects.get(pk=pk) is not None:
                        lodgingPhoto.objects.get(pk=pk).delete()
            if request.FILES.getlist('photos'):
                addImageList = request.FILES.getlist('photos')
                for addImage in addImageList:
                    lodgingPhoto.objects.create(
                        lodging=lodging, image=addImage)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description='No content'),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description='Not found')
        }
    )
    def delete(self, request, pk, format=None):
        lodging = lodgingMain.objects.get(pk=pk)
        lodging.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class lodgingReviewListView(APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: reviewSerializer})
    def get(self, request, pk, format=None):
        try:
            lodging = lodgingMain.objects.get(pk=pk)

            # 숙소에 해당하는 리뷰들 가져오기
            reviews = review.objects.filter(lodging=lodging)
            paginator = reviewListPagination()
            paginated_reviews = paginator.paginate_queryset(reviews, request)
            serializer = reviewSerializer(paginated_reviews, many=True)

            return paginator.get_paginated_response(serializer.data)
        except lodgingMain.DoesNotExist:
            return Response({"error": "Lodging not found."}, status=status.HTTP_404_NOT_FOUND)


class createReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'score': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'lodgingPk': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'score': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                        'content': openapi.Schema(type=openapi.TYPE_STRING),
                        'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                        'createdAt': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'userName': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )
    def post(self, request, format=None):
        serializer = reviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            # 숙박 정보의 pk를 요청 데이터에서 가져옵니다.
            lodgingPk = request.data.get('lodgingPk')
            try:
                lodging = lodgingMain.objects.get(pk=lodgingPk)
                # 사용자의 세션에서 인증 정보를 확인하고 user에 할당합니다.
                if request.user.is_authenticated:
                    # lodging 정보와 user 정보를 serializer에 전달해줍니다.
                    serializer.save(user=request.user, lodging=lodging)
                    # reviews = review.objects.filter(lodging=lodging)
                    # serialized_reviews = reviewSerializer(reviews, many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Authentication failed."}, status=status.HTTP_401_UNAUTHORIZED)
            except lodgingMain.DoesNotExist:
                return Response({"error": "Lodging not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class editReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=reviewCreateSerializer,
        responses={
            status.HTTP_200_OK: reviewCreateSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request')
        }
    )
    def put(self, request, pk):
        try:
            existing_review = review.objects.get(pk=pk)  # 기존 리뷰 가져오기
            serializer = reviewCreateSerializer(
                existing_review, data=request.data)  # 기존 리뷰에 데이터 업데이트
            if serializer.is_valid():
                # lodgingPk = request.data.get('lodgingPk')

                # lodging = lodgingMain.objects.get(pk=lodgingPk)
                if request.user.is_authenticated:
                    serializer.save(user=request.user)
                    return Response(serializer.data)
                else:
                    return Response({"error": "Authentication failed."}, status=status.HTTP_401_UNAUTHORIZED)

        except review.DoesNotExist:
            return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rev = review.objects.get(pk=pk)
        rev.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class lodgingScrapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'lodging': openapi.Schema(type=openapi.TYPE_INTEGER),
                'isScrap': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
            required=['lodging', 'isScrap'],
        )
    )
    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id
        lodging_pk = data.get('lodging')
        # lodging과 user가 같은 객체가 존재한다면 업데이트(덮어 쓰기)
        scrap, created = lodgingScrap.objects.update_or_create(
            lodging=lodgingMain.objects.get(pk=lodging_pk),
            user=CustomUser.objects.get(pk=request.user.id),
            defaults={'isScrap': data.get('isScrap')}
        )

        serializer = lodgingScrapSerializer(scrap)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class myPageLodgingScrapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        scraps = lodgingScrap.objects.filter(user=user, isScrap=True)
        lodgings = []
        for scrap in scraps:
            lodgings.append(lodgingMain.objects.get(pk=scrap.lodging.pk))
        serializer = lodgingMainSerializer(
            lodgings, many=True, context={'request': request})
        return Response(serializer.data)

class mainPageLodgingView(APIView):
    def get(self, request, format=None):
        top_lodgings = lodgingMain.objects.annotate(scrap_count=Count('lodgingScrap', filter=Q(lodgingScrap__isScrap=True))).order_by('-scrap_count')[:10]
        serializer = lodgingMainSerializer(
            top_lodgings, many=True, context={'request': request})
        
        return Response(serializer.data)
