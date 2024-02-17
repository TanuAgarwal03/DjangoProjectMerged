from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _  

class User(AbstractUser):
   country = models.CharField(max_length=30 , blank=True)
   dob = models.DateField(null=False, blank=False, default=timezone.now)
   state = models.CharField(max_length=20 , blank= True)
   image= models.ImageField(upload_to=None , height_field=None, width_field=None , blank=True , default=None)

class Category(models.Model):
    
    title = models.CharField(max_length=100, unique= True)
    slug = AutoSlugField(populate_from="title", unique=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title= models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.title


class Post(models.Model): #object
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,blank=True, null=True,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from ='title' , unique = True, null = True , default=None )
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumbnails = models.ImageField(upload_to='thumbnails/', default=None)
    featured_image = models.ImageField(upload_to='uploads/', default= None)
    tag = models.ManyToManyField(Tag,  blank= True)

    def __str__(self):
        return self.title

#  def save(self, **kwargs):
    #     try:
    #         kwargs['force_insert'] = True
    #         im = Image.open(self.post_content)

    #         output = BytesIO()
    #         output1= BytesIO()

    #         img = Image.open(self.post_content)

    #         if img.height > 300 or img.width >300 :
    #             output_size =(300,169)   
    #             img.thumbnail(output_size)
    #             img.save(output1, format = 'JPEG' , quality=90)
            
    #         im = im.resize((400,250))

    #         im.save(output, format='JPEG' , quality=90)
    #         output.seek(0)
    #         unique_id =get_random_string(length=32)

    #         self.post_content = InMemoryUploadedFile(output, 'ImageField' , "%s.jpg" % unique_id, 'image.jpeg', sys.getsizeof(output1), None)

    #         super(Post , self).save()
    #     except:
    #         super(Post , self).save()
    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()




