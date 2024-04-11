from django.contrib.auth.signals import user_logged_in , user_logged_out
from django.dispatch import receiver
from .models import *
from django.utils import timezone

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserLoginLogout.objects.create(user=user, login_time=timezone.now())
    print(f"User {user.username} logged in.")

@receiver(user_logged_out)
def handle_user_logout(sender, request , user, **kwargs ):
    user_login_logout = UserLoginLogout.objects.filter(user=user, logout_time__isnull=True).first()
    if user_login_logout:
        user_login_logout.logout_time = timezone.now()
        user_login_logout.save()
    print(f"User {user.username} logged out")