# Generated by Django 5.0.3 on 2024-04-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='audio',
            field=models.FileField(blank=True, default=None, null=True, upload_to='audio_files/'),
        ),
    ]
