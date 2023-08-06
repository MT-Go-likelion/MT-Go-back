from rest_framework import serializers
from .models import recreationMain, recreationScrap

class recreationMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = recreationMain
        fields = '__all__'

class createRecreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = recreationMain
        fields = ['name', 'content', 'headCountMin', 'headCountMax', 'photo']

