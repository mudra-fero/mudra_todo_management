from django.db import models
from lib.base import BaseModel
from lib.enum import LifecycleStage, PriorityLevel
from apps.users.models import UserProfile


class BaseModelWithLogs(BaseModel):
    class Meta:
        abstract = True
        ordering = ("-modified",)

    def add_history(self, task, message, user):
        TaskHistory.objects.create(
            task=task,
            user=user,
            action=message,
        )

    def add_notification(self, task, message, acting_user):
        task = (
            Task.objects.select_related("assigned_to", "created_by")
            .prefetch_related("task_collaborations")
            .get(id=task.id)
        )
        user_ids = set()
        if task.assigned_to:
            user_ids.add(task.assigned_to.id)
        if task.created_by:
            user_ids.add(task.created_by.id)
        user_ids.update(task.task_collaborations.values_list("user_id", flat=True))
        user_ids.discard(acting_user.id)
        notifications = [
            Notification(user_id=user_id, message=message) for user_id in user_ids
        ]
        Notification.objects.bulk_create(notifications)


class Task(BaseModelWithLogs):
    title = models.CharField(max_length=150)
    description = models.TextField()
    lifecycle_stage = models.IntegerField(
        choices=LifecycleStage.choices, default=LifecycleStage.TO_DO
    )
    priority = models.IntegerField(
        choices=PriorityLevel.choices, default=PriorityLevel.LOW
    )
    deadline = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        UserProfile, related_name="created_tasks", on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        UserProfile, related_name="assigned_tasks", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.title


class TaskCollaborator(BaseModelWithLogs):
    task = models.ForeignKey(
        Task, related_name="task_collaborations", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile, related_name="task_collaborations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.task.title} - Collaborator: {self.user.user.username}"


class Comment(BaseModelWithLogs):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        UserProfile, related_name="task_comments", on_delete=models.CASCADE
    )
    content = models.TextField()

    def __str__(self):
        return f"{self.author.user.username} on {self.task.title}"


class TaskHistory(BaseModelWithLogs):
    task = models.ForeignKey(
        Task, related_name="task_history", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile, related_name="user_history", on_delete=models.SET_NULL, null=True
    )
    action = models.TextField()

    def __str__(self):
        return f"History for {self.task.title} by {self.user.user.username}"


class Notification(BaseModel):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user.username} - {self.message[:30]}"
