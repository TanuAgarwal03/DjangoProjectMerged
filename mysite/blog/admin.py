from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Post
from .models import Category
from .models import Tag

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)


