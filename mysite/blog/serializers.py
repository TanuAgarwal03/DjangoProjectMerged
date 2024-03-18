from .models import * 
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return user

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key 


class PostSerializer(serializers.ModelSerializer):
    authors = UserSerializer(source='author', read_only=True, context={'request': None})

    class Meta:
        model = Post
        fields = '__all__'
      
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Username or email does not exist.')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password.')

        if not user.is_active:
            raise serializers.ValidationError('status of user is not active.')

        data['user'] = user
        return data
    
    def create(self, validated_data):
        user = validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data  
    
        return {'user': {**user_data, 'token': token.key}}

    def to_representation(self, instance):
        return instance


        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']