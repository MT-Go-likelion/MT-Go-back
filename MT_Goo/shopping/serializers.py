from rest_framework import serializers
from .models import shoppingMain

class shoppingMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = '__all__'

class createShoppingSerializer(serializers.ListSerializer):
    class Meta:
        model = shoppingMain
        fields = ['item', 'price', 'amount']
        
    def create(self, validated_data_list):
        user = self.context['request'].user
        shopping_list = []

        for validated_data in validated_data_list:
            validated_data['user'] = user
            shopping_instance = self.child.Meta.model(**validated_data)
            shopping_list.append(shopping_instance)
    
        return super().bulk_create(shopping_list)

