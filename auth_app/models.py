from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    is_banned = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
