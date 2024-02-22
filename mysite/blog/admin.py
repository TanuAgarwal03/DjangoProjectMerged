from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Post
from .models import Category
from .models import Tag
from .models import Comment
import csv
from django.http import HttpResponse

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow([
             'Username',
             'Email',
             'First Name',
             'Last Name',
             'Gender',
             'Date_of_Birth',
             'State',
             'Country',
             'Image'
             ]
            )

        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.gender,
                user.dob,
                user.state,
                user.country,
                user.image
            ])

        return response

    export_as_csv.short_description = "Export selected users as CSV"
    

class CustomPostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title' , 'created_date','published_date' )
    list_filter = ["published_date","tag" , "category"]
    filter_horizontal = ('tag',)
    search_fields = ('title', 'author',)

    def view_on_site(self, obj):
        url = reverse("blog:post_detail", kwargs={"post_slug": obj.post_slug})
        return url
   
    
class CustomCategoryAdmin(admin.ModelAdmin):
    model = Category
    list_filter = ['title']
    search_fields = ('title',)
    def has_delete_permission(self, request, obj=None):
        return False
    
  
class CustomTagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ('title',)
    list_filter = ['title']
    def has_delete_permission(self, request, obj=None):
        return False

class CustomCommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['name','post','text','body']
    list_filter = ["created"]
    search_fields = ('text',)

admin.site.register(User ,CustomUserAdmin)
admin.site.register(Post,CustomPostAdmin)
admin.site.register(Category,CustomCategoryAdmin)
admin.site.register(Tag,CustomTagAdmin)
admin.site.register(Comment,CustomCommentAdmin)


