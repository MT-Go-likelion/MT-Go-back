from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, suggestion

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'name']
        extra_kwargs = {
            'password': {'write_only': True}  # 비밀번호 필드가 응답에 포함되지 않도록 설정합니다.
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
        else:
            raise serializers.ValidationError('Incorrect credentials. Please try again.')
        return data
    
class suggestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.email')

    class Meta:
        model = suggestion
        fields = ['user', 'content', 'createdAt']

    def create(self, validated_data):
        user = self.context.get('request').user
        suggestion_obj = suggestion.objects.create(user=user, **validated_data)
        return suggestion_obj
    
class DummySerializer(serializers.Serializer):
    pass