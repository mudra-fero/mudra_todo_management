from django.db import models


class Roles(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    MANAGER = "MANAGER", "Manager"
    TEAM_MEMBER = "TEAM_MEMBER", "Team Member"


class LifecycleStage(models.IntegerChoices):
    TO_DO = 1, "To Do"
    IN_PROGRESS = 2, "In Progress"
    REVIEW = 3, "Review"
    COMPLETED = 4, "Completed"


class PriorityLevel(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"
    CRITICAL = 4, "Critical"
