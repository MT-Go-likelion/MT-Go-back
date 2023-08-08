from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import shoppingMain
from .serializers import shoppingMainSerializer, createShoppingSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication

class shoppingMainView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={status.HTTP_200_OK: shoppingMainSerializer(many=True)})
    def get(self, request, format=None):
        shopping = shoppingMain.objects.filter(user=request.user)
        serializer = shoppingMainSerializer(shopping, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class createShoppingView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,  # 리스트 형태로 요청 받음
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'item': openapi.Schema(type=openapi.TYPE_STRING),
                    'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
                required=['item', 'price', 'amount'],
            ),
        )
    )
    def post(self, request, format=None):
        shoppingList = shoppingMain.objects.filter(user=request.user)
        for shopping in shoppingList:
            shopping.delete()
        serializer = createShoppingSerializer(data=request.data, context={'request': request}, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
