from django.db import models
from django.conf import settings
from lib.enum import LifecycleStage, PriorityLevel


class TaskAssignment(models.Model):
    task = models.ForeignKey(
        "Task",
        related_name="task_assignments",
        on_delete=models.CASCADE,
        verbose_name="Task",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="task_assignments",
        on_delete=models.CASCADE,
        verbose_name="Assigned User",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} -> {self.user.username}"


class TaskCollaborator(models.Model):
    task = models.ForeignKey(
        "Task",
        related_name="task_collaborations",
        on_delete=models.CASCADE,
        verbose_name="Task",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="task_collaborations",
        on_delete=models.CASCADE,
        verbose_name="Collaborator",
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - Collaborator: {self.user.username}"


class Task(models.Model):
    title = models.CharField(max_length=150, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    lifecycle_stage = models.IntegerField(
        choices=LifecycleStage.choices,
        default=LifecycleStage.TO_DO,
        verbose_name="Lifecycle Stage",
    )
    priority = models.IntegerField(
        choices=PriorityLevel.choices,
        default=PriorityLevel.LOW,
        verbose_name="Priority",
    )
    deadline = models.DateField(null=True, blank=True, verbose_name="Deadline")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_tasks",
        on_delete=models.CASCADE,
        verbose_name="Created By",
    )
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="TaskAssignment",
        related_name="assigned_tasks",
        verbose_name="Assigned To",
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="TaskCollaborator",
        related_name="collaborated_tasks",
        verbose_name="Collaborators",
    )

    def __str__(self):
        return self.title
