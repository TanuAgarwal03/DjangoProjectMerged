from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db import models
from autoslug import AutoSlugField

from gtts import gTTS
import os

Gender_choices=[
    ('M', 'Male'),
    ('F','Female'),
]

Country_choices=[
    ('CN', 'China'),
    ('IN', 'India'),
    ('US', 'United States'),
    ('ID', 'Indonesia'),
    ('PK', 'Pakistan'),
    ('BR', 'Brazil'),
    ('NG', 'Nigeria'),
    ('BD', 'Bangladesh'),
    ('RU', 'Russia'),
    ('MX', 'Mexico'),
    ('JP', 'Japan'),
    ('ET', 'Ethiopia'),
    ('PH', 'Philippines'),
    ('EG', 'Egypt'),
    ('VN', 'Vietnam'),
    ('CD', 'Democratic Republic of the Congo'),
    ('TR', 'Turkey'),
    ('IR', 'Iran'),
    ('DE', 'Germany'),
    ('TH', 'Thailand'),
    ('GB', 'United Kingdom'),
    ('FR', 'France'),
    ('IT', 'Italy'),
    ('TZ', 'Tanzania'),
    ('ZA', 'South Africa'),
    ('KR', 'South Korea'),
    ('CO', 'Colombia'),
    ('KE', 'Kenya'),
    ('AR', 'Argentina'),
    ('UA', 'Ukraine'),
    ('SD', 'Sudan'),
    ('PL', 'Poland'),
    ('DZ', 'Algeria'),
    ('CA', 'Canada'),
    ('UG', 'Uganda'),
    ('MA', 'Morocco'),
    ('PE', 'Peru'),
    ('IQ', 'Iraq'),
    ('SA', 'Saudi Arabia'),
    ('UZ', 'Uzbekistan'),
    ('MY', 'Malaysia'),
    ('VE', 'Venezuela'),
    ('AF', 'Afghanistan'),
    ('GH', 'Ghana'),
    ('NP', 'Nepal'),
    ('YE', 'Yemen'),
    ('KP', 'North Korea'),
    ('MG', 'Madagascar'),
    ('CM', 'Cameroon'),
    ('CI', 'Ivory Coast'),
    ('AU', 'Australia'),
    ('NE', 'Niger'),
    ('TW', 'Taiwan'),
    ('LK', 'Sri Lanka'),
    ('BF', 'Burkina Faso'),
    ('ML', 'Mali'),
    ('RO', 'Romania'),
    ('MW', 'Malawi'),
    ('CL', 'Chile'),
    ('KZ', 'Kazakhstan'),
    ('ZM', 'Zambia'),
    ('GT', 'Guatemala'),
    ('EC', 'Ecuador'),
    ('SY', 'Syria'),
    ('NL', 'Netherlands'),
    ('SN', 'Senegal'),
    ('KP', 'Cambodia'),
    ('TD', 'Chad'),
    ('SO', 'Somalia'),
    ('ZW', 'Zimbabwe'),
    ('RW', 'Rwanda'),
    ('GN', 'Guinea'),
    ('BJ', 'Benin'),
    ('TN', 'Tunisia'),
    ('BE', 'Belgium'),
    ('CU', 'Cuba'),
    ('BO', 'Bolivia'),
    ('HT', 'Haiti'),
    ('GR', 'Greece'),
    ('DO', 'Dominican Republic'),
    ('CZ', 'Czech Republic'),
    ('PT', 'Portugal'),
    ('SV', 'El Salvador'),
    ('HN', 'Honduras'),
]

class User(AbstractUser):
   gender = models.CharField(max_length=1,choices= Gender_choices ,blank=True)
   country = models.CharField(max_length=2 ,choices= Country_choices, blank=True,default= 'IN')
   dob = models.DateField(null=False, blank=False, default=timezone.now)
   state = models.CharField(max_length=20 , blank= True)
   image= models.ImageField(upload_to='profile_images/'  , blank=True , default="Screenshot_24.png")
  
   def __str__(self):
       return self.username

   def image_preview(self):
       return mark_safe('<img src = "{url}" width = "50"/>'.format(
        url = self.image.url))

   def image_preview2(self): 
        return mark_safe('<img src = "{url}" width = "70"/>'.format(
             url = self.image.url
         ))

   def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Category(models.Model):
    title = models.CharField(max_length=100, unique= True)
    slug = AutoSlugField(populate_from="title", unique=True)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Tag(models.Model):
    title= models.CharField(max_length=100,unique=True)
    slug = AutoSlugField(populate_from="title", unique=True, null = True , default=None)
    
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,blank=True, null=True,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from ='title' , unique = True, null = True , default=None )
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumbnails = models.ImageField(upload_to='thumbnails/', default=None)
    featured_image = models.ImageField(upload_to='uploads/', default= None)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def get_comments(self):
        return Comment.objects.filter(post=self, parent__isnull=True, active=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail' ,kwargs={"slug": self.slug})
    
    # def generate_speech(self):
    #     tts = gTTS(text=self.text, lang='en')
    #     audio_file_path = os.path.join('audio_files', f'{self.slug}.mp3')
    #     tts.save(audio_file_path)
    #     return audio_file_path
    
    def generate_speech(self):
        tts = gTTS(text=self.text, lang='en')

        # Create the directory if it doesn't exist
        directory = os.path.join(settings.MEDIA_ROOT, 'audio_files')
        if not os.path.exists(directory):
            os.makedirs(directory)

        audio_file_path = os.path.join(directory, f'{self.slug}.mp3')
        tts.save(audio_file_path)
        return audio_file_path

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    name = models.CharField(max_length=50)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self) :
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

    









