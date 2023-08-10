from rest_framework import serializers
from .models import *
from lodging.models import lodgingMain
class teamSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamSpace
        fields = ['teamName', 'teamToken']

class teamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamUser
        fields = '__all__'

class teamLodgingScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamLodgingScrap
        fields = '__all__'


class teamScrapListSerializer(serializers.ModelSerializer):
    isScrap = serializers.SerializerMethodField()
    class Meta:
        model = teamSpace
        fields = ['teamName', 'teamToken', 'isScrap']
    def get_isScrap(self, obj):
        scrapedTeam = self.context.get('scrapedTeam', [])  # context에서 scrapedTeam 정보를 가져옵니다.
        return obj in scrapedTeam

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
