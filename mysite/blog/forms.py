from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django import forms

from .models import Post
from .models import User
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)

# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = MyUser
#         fields = ("username" , "email")

# class LogInForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)