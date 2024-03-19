from .models import * 
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name' , 'email', 'gender' , 'country' , 'state' ,'dob' , 'image' ,'token','id']
        extra_kwargs = {
            'password': {'write_only': True },
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The password and confirm password do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from validated_data
        user = User.objects.create_user(**validated_data)
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