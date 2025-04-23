import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    assigned_to = django_filters.NumberFilter(field_name="assigned_to__id")
    stage = django_filters.CharFilter(field_name="lifecycle_stage")
    priority = django_filters.CharFilter(field_name="priority")
    deadline = django_filters.DateFilter(field_name="deadline")

    class Meta:
        model = Task
        fields = ["assigned_to", "stage", "priority", "deadline"]
