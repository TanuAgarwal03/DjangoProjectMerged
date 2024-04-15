from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django import forms
from django.db import models
from .models import Post
from .models import User
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'title', 'text', 'category', 'tags' ,'thumbnails','featured_image') 
        # fields ='__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2', 'first_name', 'last_name', 'dob','gender','state','country')
        widgets ={
            'dob': forms.widgets.DateInput(attrs={'type': 'date'})
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email" ,"first_name" , "last_name" , "state", "country", "dob" , 'gender' , 'image' )
        widgets ={
            'dob': forms.widgets.DateInput(attrs={'type': 'date'})
        }

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    class Meta:
        model = Post
        fields =['username','password1' ,'password2']
        

class AuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name","body")

class TestingForm(forms.ModelForm):
    class Meta:
        model = Testing
        fields = '__all__'
        widgets ={
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'time': forms.widgets.TimeInput(attrs={'type': 'time'}),
            'published' : forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BulkPostUploadForm(forms.Form):
    excel_file = forms.FileField()