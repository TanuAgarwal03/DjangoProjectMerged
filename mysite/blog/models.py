from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.base_user import BaseUserManager

class User(AbstractUser):
   country = models.CharField(max_length=30 , blank=True)
   dob = models.DateField(null=False, blank=False, default=timezone.now)
   state = models.CharField(max_length=20 , blank= True)
   image= models.ImageField(upload_to=None , height_field=None, width_field=None , blank=True , default=None)

#    REQUIRED_FIELDS= ['country' , 'dob', 'state']

class Post(models.Model): #object
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from ='title' , unique = True, null = True , default=None )
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    post_content = models.FileField(max_length=200, upload_to='Video/', null= True, default=None)
    thumbnails = models.FileField(max_length=300, upload_to='thumbnails/',null=True , default= None)
    faetured_image = models.ImageField(upload_to='featured_image/%Y/%m/%d/')

    def save(self, **kwargs):
        try:
            kwargs['force_insert'] = True
            im = Image.open(self.post_content)

            output = BytesIO()
            output1= BytesIO()

            img = Image.open(self.post_content)

            if img.height > 300 or img.width >300 :
                output_size =(300,169)   
                img.thumbnail(output_size)
                img.save(output1, format = 'JPEG' , quality=90)
            
            im = im.resize((400,250))

            im.save(output, format='JPEG' , quality=90)
            output.seek(0)
            unique_id =get_random_string(length=32)

            self.post_content = InMemoryUploadedFile(output, 'ImageField' , "%s.jpg" % unique_id, 'image.jpeg', sys.getsizeof(output1), None)

            super(Post , self).save()
        except:
            super(Post , self).save()
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



