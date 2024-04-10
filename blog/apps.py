from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
# from blog.signals import *

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    # def ready(self):
    #     from . import signals
