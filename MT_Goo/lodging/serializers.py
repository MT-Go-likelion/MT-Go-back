from rest_framework import serializers
from .models import lodgingMain, lodgingPhoto, review, priceByDate

class lodgingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = lodgingPhoto
        fields = '__all__'
    
class lodgingMainSerializer(serializers.ModelSerializer):
    # 평균 점수를 계산하여 평균_score 필드에 추가
    avgScore = serializers.SerializerMethodField()
    mainPhoto = serializers.SerializerMethodField()
    class Meta:
        model = lodgingMain
        fields = ['pk', 'name', 'place', 'price', 'headCount', 'mainPhoto', 'avgScore']

    def get_avgScore(self, obj):
        # 숙소에 연결된 리뷰들의 점수 평균 계산
        reviews = review.objects.filter(lodging=obj)
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            avgScore = total_score / reviews.count()
            return avgScore
        else:
            return 0
        
    def get_mainPhoto(self, lodging):
        if lodging.mainPhoto:
            return lodging.mainPhoto.url
        else:
            return None

class reviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = ['score', 'image', 'contents']

class reviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = ['score', 'image', 'contents']

    # image 필드의 URL을 직렬화하기 위해 다음과 같이 to_representation 메서드를 오버라이드합니다.
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.image:
            # 이미지 필드의 URL을 직렬화하여 반환합니다.
            ret['image'] = instance.image.url
        return ret

class priceByDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = priceByDate
        fields = ['date', 'price']

class lodgingDetailSerializer(serializers.ModelSerializer):
    photos = lodgingPhotoSerializer(many=True)  # Use the modified lodgingPhotoSerializer
    reviews = reviewSerializer(many=True, required=False)
    prices_by_date = serializers.SerializerMethodField()
    mainPhoto = serializers.SerializerMethodField()

    class Meta:
        model = lodgingMain
        fields = ['pk', 'name', 'address', 'place', 'price', 'phoneNumber', 'homePageURL', 'headCount', 'scrap', 'content', 'precaution', 'check_in_time', 'check_out_time', 'mainPhoto', 'photos', 'reviews', 'prices_by_date']

    def get_prices_by_date(self, lodging):
        prices_by_date = priceByDate.objects.filter(lodging=lodging)
        return priceByDateSerializer(prices_by_date, many=True).data
    
    def get_mainPhoto(self, lodging):
        if lodging.mainPhoto:
            return lodging.mainPhoto.url
        else:
            return None



class lodgingCreateSerializer(serializers.ModelSerializer):
    # photos = lodgingPhotoSerializer(many=True)

    class Meta:
        model = lodgingMain
        fields = '__all__'

    # def create(self, validated_data):
    #     photos_data = validated_data.pop('photos', [])
    #     lodging = lodgingMain.objects.create(**validated_data)

    #     for photo_data in photos_data:
    #         lodgingPhoto.objects.create(lodging=lodging, **photo_data)

    #     return lodging




