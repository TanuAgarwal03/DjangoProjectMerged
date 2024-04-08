# Generated by Django 5.0.3 on 2024-04-01 10:27

import autoslug.fields
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='title', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('country', models.CharField(blank=True, choices=[('CN', 'China'), ('IN', 'India'), ('US', 'United States'), ('ID', 'Indonesia'), ('PK', 'Pakistan'), ('BR', 'Brazil'), ('NG', 'Nigeria'), ('BD', 'Bangladesh'), ('RU', 'Russia'), ('MX', 'Mexico'), ('JP', 'Japan'), ('ET', 'Ethiopia'), ('PH', 'Philippines'), ('EG', 'Egypt'), ('VN', 'Vietnam'), ('CD', 'Democratic Republic of the Congo'), ('TR', 'Turkey'), ('IR', 'Iran'), ('DE', 'Germany'), ('TH', 'Thailand'), ('GB', 'United Kingdom'), ('FR', 'France'), ('IT', 'Italy'), ('TZ', 'Tanzania'), ('ZA', 'South Africa'), ('KR', 'South Korea'), ('CO', 'Colombia'), ('KE', 'Kenya'), ('AR', 'Argentina'), ('UA', 'Ukraine'), ('SD', 'Sudan'), ('PL', 'Poland'), ('DZ', 'Algeria'), ('CA', 'Canada'), ('UG', 'Uganda'), ('MA', 'Morocco'), ('PE', 'Peru'), ('IQ', 'Iraq'), ('SA', 'Saudi Arabia'), ('UZ', 'Uzbekistan'), ('MY', 'Malaysia'), ('VE', 'Venezuela'), ('AF', 'Afghanistan'), ('GH', 'Ghana'), ('NP', 'Nepal'), ('YE', 'Yemen'), ('KP', 'North Korea'), ('MG', 'Madagascar'), ('CM', 'Cameroon'), ('CI', 'Ivory Coast'), ('AU', 'Australia'), ('NE', 'Niger'), ('TW', 'Taiwan'), ('LK', 'Sri Lanka'), ('BF', 'Burkina Faso'), ('ML', 'Mali'), ('RO', 'Romania'), ('MW', 'Malawi'), ('CL', 'Chile'), ('KZ', 'Kazakhstan'), ('ZM', 'Zambia'), ('GT', 'Guatemala'), ('EC', 'Ecuador'), ('SY', 'Syria'), ('NL', 'Netherlands'), ('SN', 'Senegal'), ('KP', 'Cambodia'), ('TD', 'Chad'), ('SO', 'Somalia'), ('ZW', 'Zimbabwe'), ('RW', 'Rwanda'), ('GN', 'Guinea'), ('BJ', 'Benin'), ('TN', 'Tunisia'), ('BE', 'Belgium'), ('CU', 'Cuba'), ('BO', 'Bolivia'), ('HT', 'Haiti'), ('GR', 'Greece'), ('DO', 'Dominican Republic'), ('CZ', 'Czech Republic'), ('PT', 'Portugal'), ('SV', 'El Salvador'), ('HN', 'Honduras')], default='IN', max_length=2)),
                ('dob', models.DateField(default=django.utils.timezone.now)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('image', models.ImageField(blank=True, default='Screenshot_24.png', upload_to='profile_images/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='title', unique=True)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('thumbnails', models.ImageField(default=None, upload_to='thumbnails/')),
                ('featured_image', models.ImageField(default=None, upload_to='uploads/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category')),
                ('tags', models.ManyToManyField(to='blog.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('body', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
