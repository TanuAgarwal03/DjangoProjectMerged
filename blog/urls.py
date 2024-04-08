from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *
app_name='blog'


urlpatterns = [
    path('post/<slug:slug>/edit/' , views.post_edit , name= 'post_edit'),
    path('post/new/', views.post_new, name='post_new'),
    path('comment/reply/', views.reply_comment, name="reply"),
    path('post/cat', views.cat_list, name='cat_list'),
    path('post/tag', views.tag_list, name='tag_list'),
    path('tag/<str:tag_title>',views.tag_details,name='tag_post'),
    path('cat/<category_slug>',views.cat_details,name='cat_post'),
    path('post/<slug:slug>/' , views.post_detail , name = 'post_detail'),
    path('login/', views.login_view , name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view,name='logout'),
    path('index/' , views.index , name='index'),
    path('success/', views.uploadok, name= 'success'),
    path('edit_profile/' ,views.edit_profile,name='edit_profile'),
    path('user<str:username>/' ,views.user_detail,name='user_detail'),
    path('', views.post_list, name='post_list'),

    path('text-to-speech/<int:post_id>/', generate_speech_view, name='generate_speech'),
    # path('text-to-speech/', views.generate_speech_view, name='text_to_speech'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 