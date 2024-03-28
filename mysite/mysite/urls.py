from django.contrib import admin
from django.urls import include, path
from rest_framework  import routers
from blog import apiViews 
from blog.apiViews import *
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'posts' , apiViews.PostViewSet)
router.register(r'category' , apiViews.CategoryViewSet)
router.register(r'tags',apiViews.TagViewSet)
router.register(r'user', apiViews.UserViewSet)
router.register(r'login_api', LoginViewSet ,basename="login")
router.register(r'signup_api',UserSignViewSet ,basename="signup")
router.register(r'change_password', apiViews.ChangePasswordViewSet, basename="")
router.register(r'comments' ,CommentViewSet)
# router.register(r'password', apiViews.PasswordResetViewSet, basename='password-reset')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('blog/' , include('blog.urls')),
    path('' , include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('reset-password/',apiViews.PasswordReset.as_view(), name='reset-password'),
    # path('reset-password/<str:encoded_pk>/<str:token>',apiViews.ResetPassword.as_view(), name='reset-password')

]
urlpatterns += router.urls 
