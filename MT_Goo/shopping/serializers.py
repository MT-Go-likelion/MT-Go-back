from rest_framework import serializers
from .models import shoppingMain

class shoppingMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = ['pk', 'item', 'price', 'amount']

class createShoppingListSerializer(serializers.ListSerializer):

    def create(self, validated_data_list):
        user = self.context['request'].user
        shopping_list = []

        for validated_data in validated_data_list:
            validated_data['user'] = user
            shopping_instance = self.child.Meta.model(**validated_data)
            shopping_list.append(shopping_instance)
    
        return self.child.Meta.model.objects.bulk_create(shopping_list)

class createShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = ['item', 'price', 'amount']
        list_serializer_class = createShoppingListSerializer

    def create(self, validated_data):
        user = self.context['request'].user
        shopping = shoppingMain.objects.create(user=user, **validated_data)
        return shopping

