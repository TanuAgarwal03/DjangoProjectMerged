from django.contrib import admin
from django.urls import include, path
from rest_framework  import routers
from blog import apiViews 
from blog.apiViews import *
from rest_framework.authtoken import views
from django.conf.urls.static import static
from blog import views

router = routers.DefaultRouter()
router.register(r'posts' , apiViews.PostViewSet)
router.register(r'category' , apiViews.CategoryViewSet)
router.register(r'tags',apiViews.TagViewSet)
router.register(r'user', apiViews.UserViewSet)
router.register(r'login_api', LoginViewSet ,basename="login")
router.register(r'signup_api',UserSignViewSet ,basename="signup")
router.register(r'change_password', apiViews.ChangePasswordViewSet, basename="")
router.register(r'comments' ,CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('blog/' , include('blog.urls')),
    path('' , include(router.urls)),
    path('accounts/', include('allauth.urls')), 
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls 



# 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   git token