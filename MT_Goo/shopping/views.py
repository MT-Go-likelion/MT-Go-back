from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import shoppingMain
from .serializers import shoppingMainSerializer, createShoppingSerializer
from rest_framework.permissions import IsAuthenticated

class shoppingMainView(APIView):
    def get(self, request, format=None):
        shopping = shoppingMain.objects.all()
        serializer = shoppingMainSerializer(shopping, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class createShoppingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = createShoppingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
