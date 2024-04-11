from django.contrib.auth.signals import user_logged_in , user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    print(f"User {user.username} logged in.")

@receiver(user_logged_out)
def handle_user_logout(sender, request , user, **kwargs ):
    print(f"User {user.username} logged out")