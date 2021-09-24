# Generated by Django 3.2.6 on 2021-09-24 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0017_remove_comment_dislikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blocked_users', models.ManyToManyField(blank=True, related_name='_social_page_blocked_users_+', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='_social_page_members_+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('posts', models.ManyToManyField(blank=True, to='social.Post')),
                ('rules', models.ManyToManyField(blank=True, related_name='_social_page_rules_+', to='social.PageRule')),
            ],
        ),
    ]
