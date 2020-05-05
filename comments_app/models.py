from django.db import models
from django.contrib.auth.models import User
from posts_app import models as post_models

# Create your models here.
class Comment(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    post = models.ForeignKey(post_models.Post, related_name="comments", on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)

