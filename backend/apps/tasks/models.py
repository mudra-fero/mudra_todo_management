from django.db import models
from django.conf import settings
from lib.enum import LifecycleStage, PriorityLevel


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    lifecycle_stage = models.IntegerField(
        choices=LifecycleStage.choices, default=LifecycleStage.TO_DO
    )
    priority = models.IntegerField(
        choices=PriorityLevel.choices, default=PriorityLevel.LOW
    )
    deadline = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_tasks",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tasks", blank=False
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="collaborated_tasks", blank=False
    )

    def __str__(self):
        return self.title
