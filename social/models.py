from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import related
from django.db.models.fields.related import OneToOneField
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name="likes")
    dislikes = models.ManyToManyField(get_user_model(), blank=True, related_name="dislikes")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.id}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def get_likes_count(self):
        return self.likes.all().count()

    def get_dislikes_count(self):
        return self.dislikes.all().count()    

class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name="comment_likes")
    dislikes = models.ManyToManyField(get_user_model(), blank=True, related_name="comment_dislikes")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        else:
            return False     

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.comment}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"post_id": self.post.id})

    def get_likes_count(self):
        return self.likes.all().count()

    def get_dislikes_count(self):
        return self.dislikes.all().count() 

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(get_user_model(), blank=True, related_name="followers")

    def __str__(self):
        return f"{self.user.email} Profile"
    
    def get_followers(self):
        return self.followers.all()

    def get_followers_count(self):
        return self.followers.all().count()