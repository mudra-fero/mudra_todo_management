from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from lib.enum import Roles


class User(AbstractUser):
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=Roles, default="TEAM_MEMBER")

    def __str__(self):
        return f"{self.user.username} ({self.role})"
