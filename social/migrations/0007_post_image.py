# Generated by Django 3.2.6 on 2021-09-08 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/post_images'),
        ),
    ]
