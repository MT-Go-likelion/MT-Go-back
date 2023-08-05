from rest_framework import serializers
from .models import shoppingMain

class shoppingMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = '__all__'

class createShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = ['user', 'item', 'price', 'amount']