# Generated by Django 5.0.3 on 2024-04-12 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testing',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='testing',
            name='published',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='testing',
            name='time',
            field=models.TimeField(),
        ),
    ]
