from django.contrib.auth.models import AbstractUser
from django.db import models

from lib.enum import Roles


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Roles, default="TEAM_MEMBER")

    def __str__(self):
        return f"{self.username} ({self.role})"
