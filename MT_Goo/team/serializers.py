from rest_framework import serializers
from .models import *
from lodging.models import lodgingMain
class teamSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamSpace
        fields = ['teamName', 'teamToken']

class teamLodgingScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamLodgingScrap
        fields = '__all__'

class teamRecreationScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamRecreationScrap
        fields = '__all__'

class teamShoppingScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamShoppingScrap
        fields = ['item', 'price', 'amount']

class createTeamShoppingListSerializer(serializers.ListSerializer):
    def create(self, validated_data_list):
        tSpace = self.context['tSpace']
        shopping_list = []

        for validated_data in validated_data_list:
            validated_data['teamSpace'] = tSpace
            shopping_instance = self.child.Meta.model(**validated_data)
            shopping_list.append(shopping_instance)
    
        return self.child.Meta.model.objects.bulk_create(shopping_list)

class createTeamShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamShoppingScrap
        fields = ['item', 'price', 'amount']
        list_serializer_class = createTeamShoppingListSerializer

    def create(self, validated_data):
        tSpace = self.context['tSpace']
        shopping = shoppingMain.objects.create(teamSpace=tSpace, **validated_data)
        return shopping
