from django.db import models
from django.conf import settings

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    lifecycle_stage = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    deadline = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_tasks', blank=False, null=False, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_tasks', blank=False, null=False, on_delete=models.CASCADE)
    collaborators = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='collaborated_tasks', blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
