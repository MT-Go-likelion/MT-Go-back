from rest_framework import serializers
from .models import lodgingMain, lodgingPhoto, review, lodgingScrap


class lodgingScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = lodgingScrap
        fields = '__all__'


class lodgingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = lodgingPhoto
        fields = ['pk', 'image']


class lodgingMainSerializer(serializers.ModelSerializer):
    # 평균 점수를 계산하여 평균_score 필드에 추가
    isScrap = serializers.SerializerMethodField()
    avgScore = serializers.SerializerMethodField()
    mainPhoto = serializers.SerializerMethodField()

    class Meta:
        model = lodgingMain
        fields = ['pk', 'name', 'place', 'lowWeekdayPrice', 
                  'headCount', 'mainPhoto', 'avgScore', 'isScrap']

    def get_avgScore(self, obj):
        # 숙소에 연결된 리뷰들의 점수 평균 계산
        reviews = review.objects.filter(lodging=obj)
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            avgScore = total_score / reviews.count()
            avgScore_rounded = round(avgScore, 1)  # 소수점 첫째 자리까지 반올림
            return avgScore_rounded
        else:
            return 0

    def get_mainPhoto(self, lodging):
        if lodging.mainPhoto:
            return lodging.mainPhoto.url
        else:
            return None

    def get_isScrap(self, lodging):
        # 현재 로그인한 유저 정보 가져오기
        user = self.context.get('request').user
        # 유저가 로그인한 경우에만 스크랩 정보를 가져오도록 처리
        if user and user.is_authenticated:
            try:
                scraps = lodgingScrap.objects.filter(
                    user=user, lodging=lodging)
                if scraps.exists():
                    return scraps[0].isScrap  # 첫 번째 스크랩 객체의 scrap 값을 반환
            except lodgingScrap.DoesNotExist:
                pass

        return None  # 토큰이 유효하지 않거나 스크랩 레코드가 없는 경우 None을 반환


# 리뷰 작성 Serializer
class reviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = ['score', 'image', 'contents']


class reviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return super().to_representation(data)

# 리뷰 Serializer


class reviewSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()

    class Meta:
        model = review
        fields = ['pk', 'score', 'image', 'contents', 'createdAt', 'userName']
        list_serializer_class = reviewListSerializer

    # image 필드의 URL을 직렬화하기 위해 다음과 같이 to_representation 메서드를 오버라이드합니다.
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.image:
            # 이미지 필드의 URL을 직렬화하여 반환합니다.
            ret['image'] = instance.image.url
        return ret

    def get_userName(self, instance):
        userName = instance.user.name
        return userName


class lodgingDetailSerializer(serializers.ModelSerializer):
    # Use the modified lodgingPhotoSerializer
    photos = lodgingPhotoSerializer(many=True)
    mainPhoto = serializers.SerializerMethodField()
    scrapCount = serializers.SerializerMethodField()
    isScrap = serializers.SerializerMethodField()
    avgScore = serializers.SerializerMethodField()
    reviewCount = serializers.SerializerMethodField()
    class Meta:
        model = lodgingMain
        fields = ['pk', 'name', 'address', 'place', 'peakWeekendPrice', 'peakWeekdayPrice', 
                  'lowWeekendPrice', 'lowWeekdayPrice', 'phoneNumber',
                  'homePageURL', 'headCount',
                  'amenities', 'content', 'precaution', 'checkInTime', 'checkOutTime',
                  'mainPhoto', 'photos', 'scrapCount', 'isScrap', 'avgScore', 'reviewCount']

    def get_mainPhoto(self, lodging):
        if lodging.mainPhoto:
            return lodging.mainPhoto.url
        else:
            return None

    def get_scrapCount(self, obj):
        return lodgingScrap.objects.filter(lodging=obj, isScrap=True).count()

    def get_isScrap(self, lodging):
        # 현재 로그인한 유저 정보 가져오기
        user = self.context.get('request').user
        # 유저가 로그인한 경우에만 스크랩 정보를 가져오도록 처리
        if user and user.is_authenticated:
            try:
                scraps = lodgingScrap.objects.filter(
                    user=user, lodging=lodging)
                if scraps.exists():
                    return scraps[0].isScrap  # 첫 번째 스크랩 객체의 scrap 값을 반환
            except lodgingScrap.DoesNotExist:
                pass

            return False  # 토큰이 유효하지 않거나 스크랩 레코드가 없는 경우 None을 반환
        return None
    
    def get_avgScore(self, obj):
        # 숙소에 연결된 리뷰들의 점수 평균 계산
        reviews = review.objects.filter(lodging=obj)
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            avgScore = total_score / reviews.count()
            avgScore_rounded = (float)(round(avgScore, 1))  # 소수점 첫째 자리까지 반올림
            return avgScore_rounded
        else:
            return 0
        
    def get_reviewCount(self, obj):
        reviews = review.objects.filter(lodging=obj)
        if reviews.exists():
            count = reviews.count()
            return count
        else: 
            return 0

class lodgingCreateSerializer(serializers.ModelSerializer):
    photos = lodgingPhotoSerializer(many=True, required=False)

    class Meta:
        model = lodgingMain
        fields = '__all__'
