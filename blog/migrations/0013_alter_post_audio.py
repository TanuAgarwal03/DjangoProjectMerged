# Generated by Django 5.0.3 on 2024-04-10 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_post_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='audio_files/'),
        ),
    ]