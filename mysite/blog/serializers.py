from .models import * 
from rest_framework import serializers

# author = User.objects.get(pk=1)
# new_post = Post.objects.create(title='Title', author=author)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'username' ,'id']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    authors = UserSerializer(source='author', read_only=True, context={'request': None})

    class Meta:
        model = Post
        fields = '__all__'
        
# class LoginSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']