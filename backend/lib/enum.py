from django.db import models

class Roles(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    MANAGER = "MANAGER", "Manager"
    TEAM_MEMBER = "TEAM_MEMBER", "Team Member"

# class TaskState(models.IntegerChoices):
#     ADMIN = "ADMIN", "Admin"
