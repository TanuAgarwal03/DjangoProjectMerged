from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django import forms
from django.db import models
from .models import Post
from .models import User
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'category', 'tag' ,'thumbnails','featured_image') 

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
