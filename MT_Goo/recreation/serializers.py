from rest_framework import serializers
from .models import recreationMain, recreationScrap

class recreationMainSerializer(serializers.ModelSerializer):
    isScrap = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    scrapCount = serializers.SerializerMethodField()
    class Meta:
        model = recreationMain
        fields = ['pk', 'name', 'photo', 'headCountMin', 'headCountMax', 'scrapCount','isScrap']

    def get_isScrap(self, recreation):
        # 현재 로그인한 유저 정보 가져오기
        user = self.context.get('request').user
        # 유저가 로그인한 경우에만 스크랩 정보를 가져오도록 처리
        if user and user.is_authenticated:
            try:
                scraps = recreationScrap.objects.filter(
                    user=user, recreation=recreation)
                if scraps.exists():
                    return scraps[0].isScrap  # 첫 번째 스크랩 객체의 scrap 값을 반환
            except recreationScrap.DoesNotExist:
                pass
        return None  # 토큰이 유효하지 않거나 스크랩 레코드가 없는 경우 None을 반환
    
    def get_photo(self, recreation):
        if recreation.photo:
            return recreation.photo.url
        else:
            return 0
        
    def get_scrapCount(self, recreation):
        return recreation.recreationScrap.filter(isScrap=True).count()
  

class recreationDetailSerializer(serializers.ModelSerializer):
    isScrap = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    scrapCount = serializers.SerializerMethodField()
    class Meta:
        model = recreationMain
        fields = ['pk', 'name', 'content', 'photo', 'headCountMin', 'headCountMax', 'scrapCount', 'isScrap']

    def get_scrapCount(self, obj):
        return recreationScrap.objects.filter(recreation=obj, isScrap=True).count()
    
    def get_photo(self, recreation):
        if recreation.photo:
            return recreation.photo.url
        else:
            return None
        
    def get_isScrap(self, recreation):
        # 현재 로그인한 유저 정보 가져오기
        user = self.context.get('request').user
        # 유저가 로그인한 경우에만 스크랩 정보를 가져오도록 처리
        if user and user.is_authenticated:
            try:
                scraps = recreationScrap.objects.filter(
                    user=user, recreation=recreation)
                if scraps.exists():
                    return scraps[0].isScrap  # 첫 번째 스크랩 객체의 scrap 값을 반환
            except recreationScrap.DoesNotExist:
                pass

        return None  # 토큰이 유효하지 않거나 스크랩 레코드가 없는 경우 None을 반환
class createRecreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = recreationMain
        fields = '__all__'

class recreationScrapSerializer(serializers.ModelSerializer):
    recreationPk = serializers.PrimaryKeyRelatedField(
        queryset=recreationMain.objects.all(),
        source='recreation',  
        write_only=True,  
    )

    class Meta:
        model = recreationScrap
        fields = ['recreationPk', 'user', 'isScrap']
