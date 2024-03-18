from django.contrib import admin
from django.urls import include, path
from rest_framework  import routers
from blog import apiViews 
from blog.apiViews import *


router = routers.DefaultRouter()
router.register(r'posts' , apiViews.PostViewSet)
router.register(r'category' , apiViews.CategoryViewSet)
router.register(r'tags',apiViews.TagViewSet)
router.register(r'user', apiViews.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('' , include('blog.urls')),
    path('router/' , include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    
]
urlpatterns += router.urls 