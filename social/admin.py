from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post, Comment, UserProfile, Notification, Thread


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(Thread)