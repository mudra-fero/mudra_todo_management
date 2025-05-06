from django.db import models
from lib.enum import LifecycleStage, PriorityLevel
from apps.users.models import UserProfile


class TaskCollaborator(models.Model):
    task = models.ForeignKey(
        "Task", related_name="task_collaborations", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile, related_name="task_collaborations", on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - Collaborator: {self.user.user.username}"


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    lifecycle_stage = models.IntegerField(
        choices=LifecycleStage.choices, default=LifecycleStage.TO_DO
    )
    priority = models.IntegerField(
        choices=PriorityLevel.choices, default=PriorityLevel.LOW
    )
    deadline = models.DateField(null=True, blank=True)
    assigned_at = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        UserProfile, related_name="created_tasks", on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        UserProfile, related_name="assigned_tasks", on_delete=models.CASCADE, null=True
    )
    collaborators = models.ManyToManyField(
        UserProfile, through="TaskCollaborator", related_name="collaborated_tasks"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        UserProfile, related_name="task_comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.user.username} on {self.task.title}"


class TaskHistory(models.Model):
    task = models.ForeignKey(
        Task, related_name="task_history", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile, related_name="user_history", on_delete=models.SET_NULL, null=True
    )
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.task.title} by {self.user.user.username}"
