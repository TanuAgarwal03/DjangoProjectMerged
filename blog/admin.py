from django import forms
from django.db import models
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from .models import *
import csv
from django.contrib.admin.models import LogEntry
from blog.models import Testing


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username' ,'email' , 'image')
    list_filter = ["last_name","country","state" , "gender"]
    search_fields = ('username', 'country',)
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
    list_display = ('title' ,'published_date','view_on_site' )
    list_filter = ["published_date","tags" , "category"]
    filter_horizontal = ('tags',)
    search_fields = ('title', 'author',)

    def view_on_site(self, obj):    
        url = reverse("blog:post_detail", kwargs={"slug": obj.slug})
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
    list_display = ['name','post','body']
    list_filter = ["created"]
    search_fields = ('body','name')

class CustomLoginLogoutAdmin(admin.ModelAdmin):
    model = UserLoginLogout
    list_display = ['user','login_time' , 'logout_time']
    list_filter = ['user']
    search_fields =['user']

# class CustomLogEntry(admin.ModelAdmin):
#     model = LogEntry
@admin.register(LogEntry)
class CustomLogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]
class CustomTesting(admin.ModelAdmin):
    model = Testing
    list_display = [
        'name',
        'published',
    ]

    list_filter = [
        'user_fk',
        'date',
        'published',
        'country',
    ]


admin.site.register(User ,CustomUserAdmin)
admin.site.register(Post,CustomPostAdmin)
admin.site.register(Category,CustomCategoryAdmin)
admin.site.register(Tag,CustomTagAdmin)
admin.site.register(Comment,CustomCommentAdmin)
admin.site.register(UserLoginLogout,CustomLoginLogoutAdmin)
admin.site.register(Testing,CustomTesting)


