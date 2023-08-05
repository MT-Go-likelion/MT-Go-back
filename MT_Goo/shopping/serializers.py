from rest_framework import serializers
from .models import shoppingMain

class shoppingMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = '__all__'

class createShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = ['item', 'price', 'amount']

    def create(self, validated_data):
        user = validated_data.get('user')
        shopping = shoppingMain.objects.create(user=user, **validated_data)
        return shopping