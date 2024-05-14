from .models import * 
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator , PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    # password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username',  'first_name', 'last_name' , 'email', 'gender' , 'country' , 'state' ,'dob' , 'image' ,'token','id' ,'last_login' ,'is_staff' , 'is_active', 'date_joined' , 'is_superuser'  ]
        extra_kwargs = {
            # 'password': {'write_only': True},
            'last_login': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_superuser': {'read_only': True},
        }
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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True ,required=True)
    new_password = serializers.CharField(write_only=True ,required=True)
    confirm_password = serializers.CharField(write_only=True , required=True)
    
    class Meta:
        model = User
        fields = ('old_password' , 'new_password','confirm_password' )
    def validate(self , attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password" : "Passwords didn't match/"})
        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)
    post = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True, context={'request': None})  
    # parent = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields= "__all__"

    def get_post(self, object):
        post = object.post
        if post:
            return {'title': post.title}
        return None

    def get_parent(self, object):
        if object.parent:
            return CommentSerializer(object.parent).data
        return None
    
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
