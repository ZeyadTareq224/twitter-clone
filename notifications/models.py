from django.db import models
from django.contrib.auth import get_user_model
from social.models import Post, Comment, Thread


class Notification(models.Model):
    # 1 = Like ,2 = Comment ,3 = Follow, 4 = DM
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(get_user_model(), related_name='notifiaction_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(get_user_model(), related_name='notifiaction_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.notification_type} from {self.from_user} to {self.to_user}"