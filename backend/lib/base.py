from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-modified",)

    @property
    def added_on(self):
        return self.created

    @property
    def updated_on(self):
        return self.modified
