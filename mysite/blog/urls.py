from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
app_name='blog'

urlpatterns = [
    # path("<slug:slug>", views.post_detail, name="post_detail"),
    # path("<slug:slug>/edit", views.post_edit, name="edit"),
    # path("<slug:slug>/post_list", views.post_list, name="post_list"),
    path('post/<slug:slug>/edit/' , views.post_edit , name= 'post_edit'),
    path('post/new/', views.post_new, name='post_new'),
    path("tag/<int:tag_id>", views.list_posts_by_tag, name="tag"),
    path("category/<slug:slug>", views.list_posts_by_category, name="category"),
    path('post/<slug:slug>/' , views.post_detail , name = 'post_detail'),
    path('success/', views.uploadok, name= 'success'),
    path('', views.post_list, name='post_list'),
    path('index/',views.index, name='home'),
    path('login/', views.login_view , name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view,name='logout'),
    path('user<str:username>/' ,views.user_detail,name='user_detail'),
    path('edit_profile/' ,views.edit_profile,name='edit_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)