from rest_framework import serializers
from .models import *
from lodging.models import lodgingMain

class teamSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamSpace
        fields = ['pk', 'teamName', 'teamToken']
    def create(self, validated_data):
        # validated_data로 받은 데이터를 사용하여 teamSpace 객체 생성
        user = self.context['request'].user
        team_space = teamSpace.objects.create(**validated_data, user=user)
    
        # 유저 정보를 가져와서 teamSpace 객체에 연결
          # request에서 유저 정보 가져오기
        team_space.save()
        return team_space

class getTeamSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = teamSpace
        fields = ['pk', 'teamName', 'teamToken', 'user']


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
        fields = ['pk', 'teamName', 'teamToken', 'isScrap']
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
