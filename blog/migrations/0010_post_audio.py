# Generated by Django 5.0.3 on 2024-04-09 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_remove_post_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='audio',
            field=models.FileField(null=True, upload_to='audio_files/'),
        ),
    ]
