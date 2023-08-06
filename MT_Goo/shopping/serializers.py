from rest_framework import serializers
from .models import shoppingMain

class shoppingMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
        fields = '__all__'

class createShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = shoppingMain
<<<<<<< Updated upstream
        fields = ['user', 'item', 'price', 'amount']
=======
        fields = ['item', 'price', 'amount']
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
>>>>>>> Stashed changes
